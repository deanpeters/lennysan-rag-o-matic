# Contributing to LennySan RAG-o-Matic

Thanks for considering contributing! This project follows a disciplined approach: **we get more done faster by focusing on less.**

## Project Philosophy

1. **One feature per version** - No scope creep, ever
2. **Low barrier** - PMs should be able to fork, clone, run
3. **Transparent costs** - Users always know what they're spending
4. **Documentation-first** - Great docs prevent support burden

## Before Contributing

1. **Check the [roadmap](README.md#roadmap)** - Is this already planned?
2. **Check existing issues** - Has someone already proposed this?
3. **Read the contracts** - Start with `contracts/0.0-9.contract/README.md`
4. **Start small** - Bug fixes and docs improvements are always welcome

## Ways to Contribute

### 🐛 Bug Fixes
- Use the [Bug Report](https://github.com/deanpeters/lennysan-rag-o-matic/issues/new/choose) template
- Include OS, Python version, error messages
- Bug fixes are always welcome via PR

### 📚 Documentation
- Fix typos, clarify instructions, add examples
- Update README if you spot outdated info
- PRs for docs don't need prior issues

### ✨ New Features
**IMPORTANT**: Open an issue FIRST using [Feature Request](https://github.com/deanpeters/lennysan-rag-o-matic/issues/new/choose) template. Do NOT start coding before discussion.

**Why?**
- Your feature might not align with project principles
- It might already be planned for a future version
- We need to agree on approach before you invest time

### 🪟 Windows Support (v3.0)
We especially need Windows contributors! If you want to own this:
1. Open an issue expressing interest
2. We'll coordinate on approach
3. You'll get credit as the Windows maintainer

## Development Setup

```bash
# Fork the repo on GitHub
git clone https://github.com/YOUR-USERNAME/lennysan-rag-o-matic
cd lennysan-rag-o-matic

# Set up dev environment
./setup.sh

# Make your changes
# Test thoroughly

# Commit with clear messages
git commit -m "fix: resolve issue with API key detection"
git push origin your-branch-name

# Open PR
```

## Code Standards

- **Python**: Follow PEP 8, use type hints where helpful
- **Error messages**: Be specific and actionable (PMs are the audience)
- **Comments**: Explain WHY, not WHAT
- **Progress indicators**: For operations >5 seconds
- **Cost transparency**: If it calls an API, mention the cost

## PR Guidelines

### Good PR Title Examples
- `fix: handle missing ANTHROPIC_API_KEY gracefully`
- `docs: clarify Windows compatibility in README`
- `feat(v0.5): add --model flag for model switching`

### Bad PR Title Examples
- `update` (too vague)
- `fix stuff` (not specific)
- `add new features` (scope creep)

### PR Checklist
- [ ] Tested on Mac (required for v0.1-2.5)
- [ ] Updated README if user-facing change
- [ ] Updated CLAUDE.md if architectural change
- [ ] Updated contracts if behavior or scope changes
- [ ] No scope creep (one feature only)
- [ ] Error messages are helpful
- [ ] Follows existing code style

## Version-Specific Guidelines

**For v0.75 (current):**
- Bug fixes only
- Docs improvements only
- No new features beyond the current scope

**For v0.5+ features:**
- Open issue first
- Wait for maintainer approval
- Implement ONLY the approved feature
- No "while I'm at it..." additions

## Questions?

Use the [Question template](https://github.com/deanpeters/lennysan-rag-o-matic/issues/new/choose) or start a [Discussion](https://github.com/deanpeters/lennysan-rag-o-matic/discussions).

## Code of Conduct

**Be kind.** This is a community tool built by PMs, for PMs. We're all learning.

- Assume good intent
- Give constructive feedback
- Help others learn
- Respect maintainer decisions

## Recognition

Contributors will be:
- Listed in release notes
- Credited in README for significant contributions
- Given ownership of areas they maintain (e.g., Windows support)

## Final Reminder

**We ship one feature at a time.** If you're wondering "should I also add...?" - the answer is NO. Ship the single feature. Move to next version.

Thanks for contributing! 🚀
