#!/usr/bin/env python3
"""
LennySan RAG-o-Matic v0.85
Simple CLI for querying Lenny's podcast corpus with metadata attribution
"""

import sys
import os
import warnings
import argparse
import copy
import json
import urllib.request
import urllib.error
import urllib.parse
import shutil
import subprocess
import re
import yaml

# Suppress LangChain deprecation warnings for v0.6
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', message='.*was deprecated.*')
try:
    from langchain_core._api.deprecation import LangChainDeprecationWarning
    warnings.filterwarnings('ignore', category=LangChainDeprecationWarning)
except Exception:
    pass

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

DEFAULT_CONFIG = {
    "version": "0.85",
    "defaults": {
        "provider": "anthropic",
        "model": "haiku",
        "response_format": "direct_inferred_missing",
        "verbose": True,
    },
    "providers": {
        "anthropic": {
            "api_key_env": "ANTHROPIC_API_KEY",
            "display_name": "Anthropic",
        },
        "openai": {
            "api_key_env": "OPENAI_API_KEY",
            "display_name": "OpenAI",
        },
    },
    "models": {
        "haiku": {
            "provider": "anthropic",
            "id": "claude-haiku-4-5-20251001",
            "label": "Claude Haiku 4.5 (cheapest)",
            "status": "active",
        },
        "sonnet-4": {
            "provider": "anthropic",
            "id": "claude-sonnet-4-20250514",
            "label": "Claude Sonnet 4 (balanced)",
            "status": "active",
        },
        "gpt-4o-mini": {
            "provider": "openai",
            "id": "gpt-4o-mini",
            "label": "GPT-4o mini (cheapest OpenAI)",
            "status": "active",
        },
        "gpt-4o": {
            "provider": "openai",
            "id": "gpt-4o",
            "label": "GPT-4o (quality OpenAI)",
            "status": "active",
        },
    },
    "paths": {
        "vector_db": "data/chroma_db",
    },
    "retrieval": {
        "search_type": "mmr",
        "k": 8,
        "fetch_k": 24,
    },
    "output": {
        "max_sources": 3,
        "response_format": "direct_inferred_missing",
        "deanisms": {
            "deanifried_response": {
                "mode": "off",
                "target_platform": "cli",
            }
        },
    },
    "features": {
        "web_search": True,
    },
    "web_search": {
        "mode": "on",
        "provider": "api",
        "endpoint": "https://google.serper.dev/search",
        "docker_endpoint": "http://localhost:8080/search",
        "allow_api_fallback": False,
        "api_key_env": "SERPER_API_KEY",
        "max_results": 5,
        "timeout_sec": 10,
    },
}


def deep_merge(base: dict, override: dict) -> dict:
    if not isinstance(override, dict):
        return base
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            base[key] = deep_merge(base[key], value)
        else:
            base[key] = value
    return base


def coerce_bool(value, default=False):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in ("true", "yes", "on", "1"):
            return True
        if lowered in ("false", "no", "off", "0"):
            return False
    return default


def load_config(path: str = "CONFIGS.yaml") -> dict:
    config = copy.deepcopy(DEFAULT_CONFIG)
    if not os.path.exists(path):
        return config
    try:
        with open(path, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f) or {}
        if isinstance(user_config, dict):
            return deep_merge(config, user_config)
    except Exception:
        pass
    return config


def build_model_catalog(config: dict) -> dict:
    providers = config.get("providers", {})
    models = config.get("models", {})
    catalog = {}
    for key, data in models.items():
        provider = data.get("provider")
        model_id = data.get("id")
        if not provider or not model_id:
            continue
        label = data.get("label")
        if not label:
            display = providers.get(provider, {}).get("display_name", provider)
            label = f"{display} ({model_id})"
        catalog[key] = {
            "provider": provider,
            "model": model_id,
            "label": label,
        }
    return catalog


def print_model_list(model_catalog: dict):
    print("Available models:")
    for key, meta in model_catalog.items():
        print(f"  {key:12} -> {meta['model']} ({meta['label']})")


def web_search_config(config: dict) -> dict:
    ws = config.get("web_search", {}) or {}
    provider = ws.get("provider", "api")
    if isinstance(provider, str):
        provider = provider.lower()
    if provider in ("serper", "api"):
        provider = "api"
    elif provider in ("searxng", "searx", "docker"):
        provider = "docker"
    docker_endpoint = ws.get("docker_endpoint", "http://localhost:8080/search")
    env_endpoint = os.environ.get("SEARXNG_ENDPOINT")
    env_port = os.environ.get("SEARXNG_PORT")
    if env_endpoint:
        docker_endpoint = env_endpoint
    elif env_port:
        docker_endpoint = f"http://localhost:{env_port}"
    return {
        "mode": ws.get("mode", "on"),
        "provider": provider,
        "endpoint": ws.get("endpoint", "https://google.serper.dev/search"),
        "docker_endpoint": docker_endpoint,
        "allow_api_fallback": coerce_bool(ws.get("allow_api_fallback", False), False),
        "api_key_env": ws.get("api_key_env", "SERPER_API_KEY"),
        "max_results": int(ws.get("max_results", 5)),
        "timeout_sec": int(ws.get("timeout_sec", 10)),
    }


def search_serper(query: str, cfg: dict) -> list[dict]:
    payload = json.dumps({"q": query}).encode("utf-8")
    req = urllib.request.Request(
        cfg["endpoint"],
        data=payload,
        headers={
            "Content-Type": "application/json",
            "X-API-KEY": cfg["api_key_env_value"],
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=cfg["timeout_sec"]) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError):
        return []

    results = []
    organic = data.get("organic", []) or []
    for item in organic[: cfg["max_results"]]:
        title = item.get("title") or ""
        link = item.get("link") or ""
        snippet = item.get("snippet") or ""
        if title or snippet or link:
            results.append({"title": title, "link": link, "snippet": snippet})
    return results


def build_searxng_url(endpoint: str, query: str) -> str:
    base = (endpoint or "").strip()
    if not base:
        base = "http://localhost:8080/search"
    if base.endswith("/search"):
        url = base
    else:
        url = base.rstrip("/") + "/search"
    params = urllib.parse.urlencode({"q": query, "format": "json"})
    return f"{url}?{params}"


def search_searxng(query: str, cfg: dict) -> tuple[list[dict], str]:
    url = build_searxng_url(cfg.get("docker_endpoint"), query)
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json,text/plain,*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "http://localhost:8080/",
        "X-Forwarded-For": "127.0.0.1",
        "X-Real-IP": "127.0.0.1",
    }
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=cfg["timeout_sec"]) as resp:
            body = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        if exc.code == 403:
            return [], "HTTP 403 from SearXNG (bot detection)"
        return [], f"HTTP {exc.code} from SearXNG"
    except urllib.error.URLError as exc:
        return [], f"Could not reach SearXNG ({exc.reason})"
    except Exception as exc:
        return [], f"Failed to reach SearXNG ({exc})"

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        snippet = body.strip().replace("\n", " ")[:200]
        return [], f"Non-JSON response from SearXNG: {snippet}"

    results = []
    for item in (data.get("results") or [])[: cfg["max_results"]]:
        title = item.get("title") or ""
        link = item.get("url") or ""
        snippet = item.get("content") or item.get("snippet") or ""
        if title or snippet or link:
            results.append({"title": title, "link": link, "snippet": snippet})
    if not results:
        return [], "SearXNG returned zero results"
    return results, ""


def searxng_ping(cfg: dict) -> tuple[bool, str]:
    url = build_searxng_url(cfg.get("docker_endpoint"), "ping")
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json,text/plain,*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "http://localhost:8080/",
        "X-Forwarded-For": "127.0.0.1",
        "X-Real-IP": "127.0.0.1",
    }
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=cfg["timeout_sec"]) as resp:
            status = resp.getcode() or 200
    except urllib.error.HTTPError as exc:
        if exc.code == 403:
            return False, "HTTP 403 from SearXNG (bot detection)"
        return False, f"HTTP {exc.code} from SearXNG"
    except urllib.error.URLError as exc:
        return False, f"Could not reach SearXNG ({exc.reason})"
    except Exception as exc:
        return False, f"Failed to reach SearXNG ({exc})"
    if status != 200:
        return False, f"HTTP {status} from SearXNG"
    return True, ""


def docker_available(timeout_sec: int = 5) -> tuple[bool, str]:
    if not shutil.which("docker"):
        return False, "Docker CLI not found"
    try:
        subprocess.run(
            ["docker", "ps"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
            timeout=timeout_sec,
        )
        return True, ""
    except subprocess.TimeoutExpired:
        return False, "Docker is not responding"
    except subprocess.CalledProcessError:
        return False, "Docker is not running"
    except OSError:
        return False, "Docker is not available"


def print_docker_help(reason: str):
    if reason == "Docker CLI not found":
        print("    Install Docker Desktop and start it once.")
        return
    print("    Start Docker Desktop:")
    print("      macOS: open -a Docker")
    print("      Windows: open Docker Desktop")
    print("    Then start SearXNG:")
    print("      docker run -d --name searxng -p 8080:8080 --restart unless-stopped searxng/searxng")
    print("    If you already created the container:")
    print("      docker start searxng")


def run_web_search(query: str, cfg: dict, api_key_value) -> tuple[list[dict], str]:
    provider = cfg.get("provider")
    if provider == "api":
        if not api_key_value:
            return [], "API key missing"
        payload_cfg = dict(cfg)
        payload_cfg["api_key_env_value"] = api_key_value
        return search_serper(query, payload_cfg), ""
    if provider == "docker":
        return search_searxng(query, cfg)
    return [], f"Unsupported provider '{provider}'"


def format_web_results(results: list[dict]) -> str:
    lines = []
    for i, item in enumerate(results, start=1):
        title = item.get("title", "").strip()
        link = item.get("link", "").strip()
        snippet = item.get("snippet", "").strip()
        line = f"{i}. {title}"
        if snippet:
            line += f" — {snippet}"
        if link:
            line += f" ({link})"
        lines.append(line)
    return "\n".join(lines)


def format_web_sources(results: list[dict]) -> str:
    lines = []
    for item in results:
        link = (item.get("link") or "").strip()
        title = (item.get("title") or "").strip() or link
        if link:
            lines.append(f"• [{title}]({link})")
    return "\n".join(lines)


def direct_answer_text(answer: str) -> str:
    lower = answer.lower()
    start = lower.find("direct answer:")
    if start == -1:
        return ""
    start = start + len("direct answer:")
    end = lower.find("indirect but relevant insights", start)
    if end == -1:
        end = len(answer)
    return answer[start:end].strip()


def parse_answer_sections(answer: str) -> dict:
    headings = {
        "direct answer": "direct",
        "indirect but relevant insights (inferred)": "indirect",
        "what's missing": "missing",
    }
    sections = {key: [] for key in headings.values()}
    current = None
    for line in answer.splitlines():
        normalized = re.sub(r"^\s*#+\s*", "", line).strip()
        normalized = normalized.rstrip(":").strip()
        lower = normalized.lower()
        if lower in headings:
            current = headings[lower]
            continue
        if current:
            sections[current].append(line)
    return {key: "\n".join(lines).strip() for key, lines in sections.items()}


def direct_is_missing(text: str) -> bool:
    stripped = text.strip().lower()
    if not stripped:
        return True
    weak_starts = (
        "not found",
        "not in provided context",
        "context does not",
        "do not know",
        "don't know",
        "cannot provide",
        "no specific",
    )
    return any(stripped.startswith(marker) for marker in weak_starts)


def deanifried_platform_rules(platform: str) -> str:
    platform = (platform or "cli").lower()
    rules = {
        "cli": "Full synthesis. 2-4 short paragraphs. No bullets in prose.",
        "x": "260-280 characters. 2-3 sentences. One paragraph only. No extra line breaks.",
        "linkedin": "1000-1300 characters. First 160 characters must stand alone. 2-3 short paragraphs.",
        "reddit": "500-1000 characters. Two short paragraphs only. Conversational tone.",
        "substack": "1000-2000 characters. 2-4 paragraphs. No paragraph over 3 sentences.",
    }
    return rules.get(platform, rules["cli"])


def run_deanifried(llm, direct: str, indirect: str, web: str, platform: str) -> str:
    platform_rules = deanifried_platform_rules(platform)
    direct_value = direct.strip() if direct else ""
    indirect_value = indirect.strip() if indirect else ""
    web_value = web.strip() if web else ""
    template = """You are writing a Dean-i-fried response (Dean Peters voice).
Blend the Direct answer and Indirect insights into one synthesis.
If the Direct answer is missing or weak, rely on Indirect and Web findings.

Voice rules (Deanisms):
- Start in motion. No preamble, no runway.
- Anthropomorphize aggressively. Give systems moods and motives.
- Coin terms without permission. Invent language shamelessly.
- Collision creates meaning. Blend 2-3 themes that shouldn't mix.
- Delight in absurdity. Escalate when it adds punch or clarity.
- Never explain the joke. Trust the reader.

Output rules:
- No emojis.
- Do not use the long em dash character (—).
- No bullet points in prose. Use sentences and short paragraphs instead.
- Do not add new facts. Stay grounded in the inputs.
- Do not include URLs or citations in the prose.
- Use mild profanity surrogates only (family-friendly). Examples: "shucks", "daggumit", "dang".
- Include at least one coined term, one anthropomorphized system, and one vivid metaphor.
- End with a short kicker line (one sentence) that lands the punch.

Platform rules:
{platform_rules}

Direct answer:
{direct}

Indirect insights:
{indirect}

Web findings (if any):
{web}

Dean-i-fried response:"""
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm | StrOutputParser()
    return chain.invoke(
        {
            "platform_rules": platform_rules,
            "direct": direct_value or "(none provided)",
            "indirect": indirect_value or "(none provided)",
            "web": web_value or "(none provided)",
        }
    )


def should_web_fallback(answer: str) -> bool:
    direct = direct_answer_text(answer).strip().lower()
    if not direct:
        return True
    if len(direct) < 40:
        return True
    weak_markers = [
        "not found",
        "not in provided context",
        "context is weak",
        "don't know",
        "do not know",
        "no specific",
        "cannot provide",
    ]
    return any(marker in direct for marker in weak_markers)


def resolve_web_search_default(features: dict, web_cfg: dict) -> str:
    mode = web_cfg.get("mode", "on")
    if isinstance(mode, str):
        mode = mode.lower()
    feature_val = features.get("web_search")
    if isinstance(feature_val, str):
        feature_val = feature_val.lower()
    if feature_val in ("on", "off", "always"):
        return feature_val
    if feature_val is False:
        return "off"
    if mode in ("on", "off", "always"):
        return mode
    return "on"


def build_llm(model_key: str, model_catalog: dict, providers: dict):
    meta = model_catalog[model_key]
    provider = meta["provider"]
    model_name = meta["model"]
    provider_meta = providers.get(provider, {})
    api_key_env = provider_meta.get("api_key_env")

    if not api_key_env:
        print(f"❌ Error: Provider '{provider}' is missing api_key_env in CONFIGS.yaml")
        return None, None

    if not os.environ.get(api_key_env):
        print(f"❌ Error: {api_key_env} not found")
        print()
        print("Set your API key:")
        print(f"  export {api_key_env}='sk-...'")
        print()
        print("Then reload your shell:")
        print("  source ~/.bashrc  (or source ~/.zshrc)")
        return None, None

    if provider == "anthropic":
        return ChatAnthropic(model=model_name, temperature=0), meta

    if provider == "openai":
        return ChatOpenAI(model=model_name, temperature=0), meta

    print(f"❌ Error: Unsupported provider: {provider}")
    return None, None

def format_sources(docs, max_sources: int = 3):
    """Format source documents with metadata into readable citations."""
    sources = []
    seen_episodes = set()
    
    for doc in docs:
        metadata = doc.metadata
        guest = metadata.get('guest', 'Unknown')
        title = metadata.get('title', 'Untitled')
        date = metadata.get('publish_date', 'Unknown date')
        youtube_url = metadata.get('youtube_url', '')
        
        # Create unique identifier to avoid duplicate citations
        episode_id = f"{guest}_{title}"
        
        if episode_id not in seen_episodes:
            seen_episodes.add(episode_id)
            citation = f"• {guest}: \"{title}\" ({date})"
            if youtube_url:
                citation += f"\n  {youtube_url}"
            sources.append(citation)
    
    return "\n".join(sources[:max_sources])


def format_docs(docs):
    """Format documents for context."""
    return "\n\n".join(doc.page_content for doc in docs)


def main():
    config = load_config()
    model_catalog = build_model_catalog(config)
    providers = config.get("providers", {})
    defaults = config.get("defaults", {})
    output_cfg = config.get("output", {}) or {}
    dean_cfg = (output_cfg.get("deanisms", {}) or {}).get("deanifried_response", {}) or {}
    model_choices = sorted(model_catalog.keys())
    default_model = defaults.get("model", "haiku")
    if default_model not in model_catalog and model_choices:
        default_model = model_choices[0]
    default_verbose = defaults.get("verbose", True)
    default_verbose_value = "on" if default_verbose else "off"
    dean_default_mode = dean_cfg.get("mode", "off")
    if isinstance(dean_default_mode, str):
        dean_default_mode = dean_default_mode.lower()
    dean_default_mode = "on" if dean_default_mode == "on" else "off"
    dean_default_platform = dean_cfg.get("target_platform", "cli")
    features = config.get("features", {})
    web_cfg = web_search_config(config)
    web_search_default = resolve_web_search_default(features, web_cfg)
    web_search_default_value = web_search_default

    parser = argparse.ArgumentParser(
        description="Query Lenny's podcast corpus with model switching",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "question",
        nargs="*",
        help="Your question in quotes (e.g., \"What does Lenny say about pricing?\")",
    )
    parser.add_argument(
        "--model",
        choices=model_choices,
        default=default_model,
        help="Model to use (see --list-models for options)",
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List available models and exit",
    )
    parser.add_argument(
        "--verbose",
        choices=["on", "off"],
        default=default_verbose_value,
        help="Verbose output (default from CONFIGS.yaml)",
    )
    parser.add_argument(
        "--web-search",
        choices=["on", "off", "always"],
        default=web_search_default_value,
        help="Web search fallback (default from CONFIGS.yaml)",
    )
    parser.add_argument(
        "--web-provider",
        choices=["api", "docker"],
        default=None,
        help="Web search provider override (api or docker)",
    )
    parser.add_argument(
        "--deanifried",
        choices=["on", "off"],
        default=dean_default_mode,
        help="Dean-i-fried response mode (default from CONFIGS.yaml)",
    )
    parser.add_argument(
        "--deanifried-platform",
        choices=["cli", "x", "linkedin", "reddit", "substack"],
        default=dean_default_platform,
        help="Dean-i-fried platform style (default from CONFIGS.yaml)",
    )

    args = parser.parse_args()

    if args.list_models:
        print_model_list(model_catalog)
        return 0

    if not args.question:
        parser.print_help()
        return 1

    verbose = args.verbose == "on"
    web_search_mode = args.web_search
    deanifried_enabled = args.deanifried == "on"
    deanifried_platform = args.deanifried_platform
    post_run_warnings = []
    web_search_requested = web_search_mode != "off"
    web_search_force = web_search_mode == "always"
    web_search_enabled = web_search_requested
    if args.web_provider:
        web_cfg["provider"] = args.web_provider
    provider = web_cfg.get("provider", "api")
    provider_label = provider.upper() if isinstance(provider, str) else "API"
    api_key_env = web_cfg.get("api_key_env", "SERPER_API_KEY")
    api_key_value = None
    if web_search_enabled:
        if provider == "api":
            api_key_value = os.environ.get(api_key_env)
            if not api_key_value:
                post_run_warnings.append(f"Web search disabled: {api_key_env} not found")
                web_search_enabled = False
        elif provider == "docker":
            ok, reason = docker_available(timeout_sec=web_cfg.get("timeout_sec", 10))
            if not ok:
                allow_api_fallback = web_cfg.get("allow_api_fallback", False)
                api_key_value = os.environ.get(api_key_env)
                if allow_api_fallback and api_key_value:
                    post_run_warnings.append("Docker not available; falling back to API search (costs apply).")
                    post_run_warnings.append("To enable Docker search, run:")
                    post_run_warnings.append("  macOS: open -a Docker")
                    post_run_warnings.append("  Windows: open Docker Desktop")
                    post_run_warnings.append("  docker run -d --name searxng -p 8080:8080 --restart unless-stopped searxng/searxng")
                    post_run_warnings.append("  docker start searxng  (if already created)")
                    post_run_warnings.append("  python explore.py --web-search always --web-provider docker \"your question here\"")
                    provider = "api"
                    provider_label = "API"
                    web_cfg["provider"] = "api"
                    web_search_enabled = True
                else:
                    if reason:
                        post_run_warnings.append(f"Web search disabled: Docker is not available ({reason})")
                    else:
                        post_run_warnings.append("Web search disabled: Docker is not available")
                    post_run_warnings.append("Start Docker Desktop, then run:")
                    post_run_warnings.append("  macOS: open -a Docker")
                    post_run_warnings.append("  Windows: open Docker Desktop")
                    post_run_warnings.append("  docker run -d --name searxng -p 8080:8080 --restart unless-stopped searxng/searxng")
                    post_run_warnings.append("  docker start searxng  (if already created)")
                    post_run_warnings.append("  python explore.py --web-search always --web-provider docker \"your question here\"")
                    if allow_api_fallback:
                        if not api_key_value:
                            post_run_warnings.append(f"API fallback disabled: {api_key_env} not found")
                    post_run_warnings.append("Install and start Docker Desktop, or switch provider to api.")
                    web_search_enabled = False
            else:
                ping_ok, ping_reason = searxng_ping(web_cfg)
                if not ping_ok:
                    allow_api_fallback = web_cfg.get("allow_api_fallback", False)
                    api_key_value = os.environ.get(api_key_env)
                    if allow_api_fallback and api_key_value:
                        post_run_warnings.append("Docker search not reachable; falling back to API search (costs apply).")
                        post_run_warnings.append(f"Reason: {ping_reason}")
                        post_run_warnings.append("To enable Docker search, run:")
                        post_run_warnings.append("  macOS: open -a Docker")
                        post_run_warnings.append("  Windows: open Docker Desktop")
                        post_run_warnings.append("  docker run -d --name searxng -p 8080:8080 --restart unless-stopped searxng/searxng")
                        post_run_warnings.append("  python explore.py --web-search always --web-provider docker \"your question here\"")
                        provider = "api"
                        provider_label = "API"
                        web_cfg["provider"] = "api"
                        web_search_enabled = True
                    else:
                        post_run_warnings.append("Web search disabled: Docker search is not reachable")
                        post_run_warnings.append(f"Reason: {ping_reason}")
                        post_run_warnings.append("Start Docker Desktop, then run:")
                        post_run_warnings.append("  macOS: open -a Docker")
                        post_run_warnings.append("  Windows: open Docker Desktop")
                        post_run_warnings.append("  docker run -d --name searxng -p 8080:8080 --restart unless-stopped searxng/searxng")
                        post_run_warnings.append("  python explore.py --web-search always --web-provider docker \"your question here\"")
                        if allow_api_fallback and not api_key_value:
                            post_run_warnings.append(f"API fallback disabled: {api_key_env} not found")
                        web_search_enabled = False
        else:
            post_run_warnings.append(f"Web search disabled: unsupported provider '{provider}'")
            web_search_enabled = False

    def vprint(*print_args, **print_kwargs):
        if verbose:
            print(*print_args, **print_kwargs)
    
    # Check if vector DB exists
    vector_db_path = config.get("paths", {}).get("vector_db", "data/chroma_db")
    if not os.path.exists(vector_db_path):
        print("❌ Error: Vector database not found")
        print()
        print("Run setup first:")
        print("  ./setup.sh")
        return 1
    
    query = " ".join(args.question).strip()
    
    vprint()
    vprint("🔍 Searching Lenny's podcast corpus...")
    vprint(f"❓ Question: {query}")
    if web_search_requested:
        mode_label = "FORCED" if web_search_force else "AUTO"
        vprint(f"🌐 Web search fallback: {'ON' if web_search_enabled else 'OFF'} ({mode_label}, {provider_label})")
    vprint()
    if deanifried_enabled:
        print(f"🎭 Dean-i-fried: ON (platform: {deanifried_platform}, extra LLM call)")
    
    try:
        # Load embeddings (same model used for indexing)
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Load vector store
        vectorstore = Chroma(
            persist_directory=vector_db_path,
            embedding_function=embeddings
        )
        
        retrieval = config.get("retrieval", {})
        retriever = vectorstore.as_retriever(
            search_type=retrieval.get("search_type", "mmr"),
            search_kwargs={
                "k": retrieval.get("k", 8),
                "fetch_k": retrieval.get("fetch_k", 24),
            },
        )
        
        llm, model_meta = build_llm(args.model, model_catalog, providers)
        if llm is None:
            return 1
        
        # Create prompt template
        response_format = config.get("output", {}).get(
            "response_format", "direct_inferred_missing"
        )
        if deanifried_enabled and response_format != "direct_inferred_missing":
            post_run_warnings.append("Dean-i-fried disabled: response_format is not direct_inferred_missing")
            deanifried_enabled = False
        if response_format == "direct_inferred_missing":
            template = """You are a helpful assistant answering questions about Lenny Rachitsky's podcast.
Use the following context from podcast transcripts to answer the question.
Respond in three sections with these headings:
Direct answer:
Indirect but relevant insights (inferred):
What's missing:

Rules:
- No bullet points in prose. Use sentences and short paragraphs.
- Minimums are not targets. If the context supports more, go longer. Do not pad with filler.
- Prefer substance over brevity. Use additional sentences when they add clarity, nuance, or helpful detail.
- Direct answer: 2-6 sentences (more if context is rich). Give a best‑effort summary grounded in the context. If the context is weak, say so, but still summarize any relevant details you can find.
- Direct answer must include at least two concrete details from the context (names, examples, outcomes, quotes, or actions). If the context does not provide two details, explicitly say that and explain what is missing.
- Indirect insights: 3-6 sentences with at least two distinct insights grounded in the context. If only one distinct insight exists, say that explicitly and explain the constraint.
- Indirect insights should include at least one concrete detail from the context. If none exist, state the limitation.
- What's missing: 1-3 sentences describing gaps or absent information.

Context:
{context}

Question: {question}

Answer:"""
        else:
            template = """You are a helpful assistant answering questions about Lenny Rachitsky's podcast.
Use the following context from podcast transcripts to answer the question.
If you don't know the answer based on the context, just say so - don't make things up.

Context:
{context}

Question: {question}

Answer:"""
        
        prompt = ChatPromptTemplate.from_template(template)
        
        # Get source documents for attribution
        source_docs = retriever.invoke(query)
        doc_context = format_docs(source_docs)

        def run_answer(context: str) -> str:
            chain = prompt | llm | StrOutputParser()
            return chain.invoke({"context": context, "question": query})

        vprint("🤔 Thinking...")

        answer = run_answer(doc_context)
        web_results = []
        web_error = ""

        if web_search_enabled:
            if web_search_force:
                vprint("🌐 Running web search (forced)...")
                web_results, web_error = run_web_search(query, web_cfg, api_key_value)
                if web_results:
                    web_context = format_web_results(web_results)
                    combined_context = doc_context + "\n\nWeb results:\n" + web_context
                    answer = run_answer(combined_context)
                else:
                    vprint("⚠️  Web search returned no results")
            else:
                if should_web_fallback(answer):
                    vprint("🌐 Running web search fallback...")
                    web_results, web_error = run_web_search(query, web_cfg, api_key_value)
                    if web_results:
                        web_context = format_web_results(web_results)
                        combined_context = doc_context + "\n\nWeb results:\n" + web_context
                        answer = run_answer(combined_context)
                    else:
                        vprint("⚠️  Web search returned no results")
                else:
                    vprint("ℹ️  Web search fallback not triggered (direct answer strong)")

        if deanifried_enabled:
            sections = parse_answer_sections(answer)
            direct_text = sections.get("direct", "")
            indirect_text = sections.get("indirect", "")
            if not indirect_text:
                indirect_text = answer.strip()
            if direct_is_missing(direct_text):
                direct_text = ""
            web_context = format_web_results(web_results) if web_results else ""
            deanifried_text = run_deanifried(
                llm=llm,
                direct=direct_text,
                indirect=indirect_text,
                web=web_context,
                platform=deanifried_platform,
            )
            if deanifried_text:
                answer = answer.rstrip() + "\n\nDean-i-fried:\n" + deanifried_text.strip()
        
        print()
        print("💡 Answer:")
        print("-" * 50)
        print(answer)
        print("-" * 50)
        print()
        
        # Show sources with metadata
        max_sources = config.get("output", {}).get("max_sources", 3)
        if source_docs:
            print("📚 Sources:")
            print(format_sources(source_docs, max_sources=max_sources))
            print()
        if web_results:
            print("🌐 Web Sources:")
            print(format_web_sources(web_results))
            print()
        if post_run_warnings:
            print("⚠️  Web search notice:")
            for line in post_run_warnings:
                print(f"  {line}")
            print()
        if verbose and web_search_requested and web_search_enabled and not web_results and web_error:
            print("🔎 Web search diagnostics:")
            print(f"  {web_error}")
            print()
        
        vprint(f"ℹ️  Using {model_meta['model']} ({model_meta['label']})")
        vprint("   Cost: varies by model")
        vprint()
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("If you're seeing API errors, check:")
        print("  - The correct API key is set for your selected model")
        print("  - You have API credits available")
        print()
        return 1

if __name__ == "__main__":
    exit(main())
