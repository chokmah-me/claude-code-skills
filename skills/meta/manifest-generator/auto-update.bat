@echo off
echo Updating Claude Code Skill Manifest...
cd /d "%USERPROFILE%\.claude\skills"
python3 meta\manifest-generator\generate_manifest_simple.py
echo Manifest update complete!
echo.
echo Current skills summary:
dir /s /b SKILL.md | find /c "SKILL.md"
echo.
pause