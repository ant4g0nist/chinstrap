import os
from ptpython.prompt_style import PromptStyle
from ptpython.layout import CompletionVisualisation
from prompt_toolkit.formatted_text import AnyFormattedText

__prompt__ = "chinstrap:> "
chinstrapRoot = os.path.expanduser("~/.chinstrap/")
historyPath = f"{chinstrapRoot}/history"

if not os.path.exists(chinstrapRoot):
    os.mkdir(chinstrapRoot)
    with open(historyPath, "w") as f:
        f.write("")


def configure(repl):
    # Configuration method. This is called during the start-up of ptpython.

    # # Show function signature (bool).
    repl.show_signature = True

    # # Show docstring (bool).
    repl.show_docstring = True

    # # Show the "[Meta+Enter] Execute" message when pressing [Enter] only
    # # inserts a newline instead of executing the code.
    repl.show_meta_enter_message = True

    # # Show completions. (NONE, POP_UP, MULTI_COLUMN or TOOLBAR)
    repl.completion_visualisation = CompletionVisualisation.MULTI_COLUMN

    repl.completion_menu_scroll_offset = 0

    repl.show_status_bar = False
    repl.show_sidebar_help = False

    # # Highlight matching parethesis.
    repl.highlight_matching_parenthesis = True

    # # Line wrapping. (Instead of horizontal scrolling.)
    repl.wrap_lines = True

    # # Complete while typing. (Don't require tab before the
    # # completion menu is shown.)
    repl.complete_while_typing = True

    # Vi mode.
    repl.vi_mode = False

    # # Paste mode. (When True, don't insert whitespace after new line.)
    # repl.paste_mode = False

    class ClassicPrompt(PromptStyle):
        """
        The classic Python prompt.
        """

        def in_prompt(self) -> AnyFormattedText:
            return [("class:prompt", __prompt__)]

        def in2_prompt(self, width: int) -> AnyFormattedText:
            return [("class:prompt.dots", "...")]

        def out_prompt(self) -> AnyFormattedText:
            return []

    # Use the classic prompt. (Display '>>>' instead of 'In [1]'.)
    repl.all_prompt_styles["custom"] = ClassicPrompt()
    repl.prompt_style = "custom"  # "ipython"  # 'classic' or 'ipython'

    # Don't insert a blank line after the output.
    repl.insert_blank_line_after_output = False

    repl.enable_history_search = True

    # Enable auto suggestions. (Pressing right arrow will complete the input,
    # based on the history.)
    repl.enable_auto_suggest = False

    # Enable open-in-editor. Pressing C-x C-e in emacs mode or 'v' in
    # Vi navigation mode will open the input in the current editor.
    repl.enable_open_in_editor = True

    # Enable system prompt. Pressing meta-! will display the system prompt.
    # Also enables Control-Z suspend.
    repl.enable_system_bindings = True

    # Ask for confirmation on exit.
    repl.confirm_exit = True

    # Enable input validation. (Don't try to execute when the input contains
    # syntax errors.)
    repl.enable_input_validation = True

    # Use this colorscheme for the code.
    repl.use_code_colorscheme("default")

    repl.color_depth = "DEPTH_8_BIT"  # The default, 256 colors.
    # repl.color_depth = "DEPTH_24_BIT"  # True color.

    # Min/max brightness
    repl.min_brightness = 0.0  # Increase for dark terminal backgrounds.
    repl.max_brightness = 1.0  # Decrease for light terminal backgrounds.

    # Syntax.
    repl.enable_syntax_highlighting = True

    # Get into Vi navigation mode at startup
    repl.vi_start_in_navigation_mode = False

    # Preserve last used Vi input mode between main loop iterations
    repl.vi_keep_last_used_mode = False

    repl.confirm_exit = False
