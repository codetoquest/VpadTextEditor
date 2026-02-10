# VpadTextEditor

A Tkinter-based text editor with formatting, themes, file operations, and **Agent Assist** tools.

## Agentic Feature: Agent Assist

Use **Agent → Open Agent Assist** (or `Ctrl+Shift+A`) to open a helper panel that can run local text intelligence actions on selected text (or the full document):

- Summarize
- Extract Action Items
- Improve Clarity
- Convert to Bullet Points
- Copy generated result to clipboard
- Apply result back into the editor

This feature runs fully local (no API key required).

## Quality updates

- Fixed window-close save flow typo (`destroy` call).
- Removed nested `mainloop()` inside the Find dialog for better Tkinter behavior.
- Added unit tests for `agent_assist.py`.
