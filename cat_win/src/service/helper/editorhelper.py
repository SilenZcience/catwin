"""
editorhelper
"""

try:
    import curses
    def initscr():
        """
        fix windows-curses for Python >= 3.12:
        https://github.com/zephyrproject-rtos/windows-curses/issues/50
        """
        import _curses
        stdscr = _curses.initscr()
        for key, value in _curses.__dict__.items():
            if key[0:4] == 'ACS_' or key in ('LINES', 'COLS'):
                setattr(curses, key, value)

        return stdscr
    curses.initscr = initscr
except ImportError:
    pass


UNIFY_HOTKEYS = {
    # (shift -) newline
    b'^M'           : b'_key_enter', # CR
    b'^J'           : b'_key_enter', # LF
    b'PADENTER'     : b'_key_enter', # numpad
    b'SHF_PADENTER' : b'_key_enter',
    b'KEY_ENTER'    : b'_key_enter', # 'fn' mode
    # ctrl - newline
    b'CTL_ENTER'    : b'_key_enter', # windows
    b'CTL_PADENTER' : b'_key_enter', # numpad

    # delete
    b'KEY_DC'       : b'_key_dc', # windows & xterm
    # b'^D'           : b'_key_dc', # some unix machines
    b'PADSTOP'      : b'_key_dc', # numpad
    # shift - delete
    b'KEY_SDC'      : b'_key_dc', # windows & xterm
    # alt - delete
    b'ALT_DEL'      : b'_key_dc', # windows
    b'kDC3'         : b'_key_dc', # xterm
    b'ALT_PADSTOP'  : b'_key_dc', # numpad
    # ctrl - del
    b'CTL_DEL'      : b'_key_dl', # windows
    b'kDC5'         : b'_key_dl', # xterm
    b'CTL_PADSTOP'  : b'_key_dl', # numpad

    # (shift -) backspace
    b'^H'           : b'_key_backspace', # windows (ctrl-backspace on xterm...)
    b'KEY_BACKSPACE': b'_key_backspace', # xterm
    # alt - backspace
    b'ALT_BKSP'     : b'_key_backspace', # windows
    # ctrl-backspace
    b'^?'           : b'_key_ctl_backspace', # windows

    # arrows
    b'KEY_LEFT'     : b'_move_key_left', # windows & xterm
    b'KEY_RIGHT'    : b'_move_key_right',
    b'KEY_UP'       : b'_move_key_up',
    b'KEY_DOWN'     : b'_move_key_down',
    b'KEY_B1'       : b'_move_key_left', # numpad
    b'KEY_B3'       : b'_move_key_right',
    b'KEY_A2'       : b'_move_key_up',
    b'KEY_C2'       : b'_move_key_down',
    # ctrl-arrows
    b'CTL_LEFT'     : b'_move_key_ctl_left', # windows
    b'CTL_RIGHT'    : b'_move_key_ctl_right',
    b'CTL_UP'       : b'_move_key_ctl_up',
    b'CTL_DOWN'     : b'_move_key_ctl_down',
    b'kLFT5'        : b'_move_key_ctl_left', # xterm
    b'kRIT5'        : b'_move_key_ctl_right',
    b'kUP5'         : b'_move_key_ctl_up',
    b'kDN5'         : b'_move_key_ctl_down',
    b'CTL_PAD4'     : b'_move_key_ctl_left', # numpad
    b'CTL_PAD6'     : b'_move_key_ctl_right',
    b'CTL_PAD8'     : b'_move_key_ctl_up',
    b'CTL_PAD2'     : b'_move_key_ctl_down',
    # shift-arrows
    b'KEY_SLEFT'    : b'_select_key_left', # windows
    b'KEY_SRIGHT'   : b'_select_key_right',
    b'KEY_SUP'      : b'_select_key_up',
    b'KEY_SDOWN'    : b'_select_key_down',
    b'KEY_SR'       : b'_select_key_up', # xterm
    b'KEY_SF'       : b'_select_key_down',
    # alt - arrows
    b'ALT_LEFT'     : b'_scroll_key_left', # windows
    b'ALT_RIGHT'    : b'_scroll_key_right',
    b'ALT_UP'       : b'_scroll_key_up',
    b'ALT_DOWN'     : b'_scroll_key_down',
    b'kLFT3'        : b'_scroll_key_left', # xterm
    b'kRIT3'        : b'_scroll_key_right',
    b'kUP3'         : b'_scroll_key_up',
    b'kDN3'         : b'_scroll_key_down',
    b'ALT_PAD4'     : b'_scroll_key_left', # numpad
    b'ALT_PAD6'     : b'_scroll_key_right',
    b'ALT_PAD8'     : b'_scroll_key_up',
    b'ALT_PAD2'     : b'_scroll_key_down',

    # page
    b'KEY_PPAGE'    : b'_move_key_page_up', # windows & xterm
    b'KEY_NPAGE'    : b'_move_key_page_down',
    b'KEY_A3'       : b'_move_key_page_up', # numpad
    b'KEY_C3'       : b'_move_key_page_down',
    # ctrl - page
    b'CTL_PGUP'     : b'_move_key_page_up', # windows
    b'CTL_PGDN'     : b'_move_key_page_down',
    b'kPRV5'        : b'_move_key_page_up', # xterm
    b'kNXT5'        : b'_move_key_page_down',
    b'CTL_PAD9'     : b'_move_key_page_up', # numpad
    b'CTL_PAD3'     : b'_move_key_page_down',
    # shift - page
    b'KEY_SPREVIOUS': b'_select_key_page_up', # windows & xterm
    b'KEY_SNEXT'    : b'_select_key_page_down',
    # alt - page
    b'ALT_PGUP'     : b'_scroll_key_page_up', # windows
    b'ALT_PGDN'     : b'_scroll_key_page_down',
    b'kPRV3'        : b'_scroll_key_page_up', # xterm
    b'kNXT3'        : b'_scroll_key_page_down',
    b'ALT_PAD9'     : b'_scroll_key_page_up', # numpad
    b'ALT_PAD3'     : b'_scroll_key_page_down',

    # end
    b'KEY_END'      : b'_move_key_end', # windows & xterm
    b'KEY_C1'       : b'_move_key_end', # numpad
    # ctrl - end
    b'CTL_END'      : b'_move_key_ctl_end', # windows
    b'kEND5'        : b'_move_key_ctl_end', # xterm
    b'CTL_PAD1'     : b'_move_key_ctl_end', # numpad
    # shift - end
    b'KEY_SEND'     : b'_select_key_end', # windows & xterm
    # alt - end
    b'ALT_END'      : b'_scroll_key_end', # windows
    b'kEND3'        : b'_scroll_key_end', # xterm
    b'ALT_PAD1'     : b'_scroll_key_end', # numpad

    # pos/home
    b'KEY_HOME'     : b'_move_key_home', # windows & xterm
    b'KEY_A1'       : b'_move_key_home', # numpad
    # ctrl - pos/home
    b'CTL_HOME'     : b'_move_key_ctl_home', # windows
    b'kHOM5'        : b'_move_key_ctl_home', # xterm
    b'CTL_PAD7'     : b'_move_key_ctl_home', # numpad
    # shift - pos/home
    b'KEY_SHOME'     : b'_select_key_home', # windows & xterm
    # alt - pos/home
    b'ALT_HOME'     : b'_scroll_key_home', # windows
    b'kHOM3'        : b'_scroll_key_home', # xterm
    b'ALT_PAD7'     : b'_scroll_key_home', # numpad

    # (shift +) tab
    b'^I'            : b'_indent_tab',
    b'KEY_BTAB'      : b'_indent_btab', # windows & xterm

    # default alnum key
    b'_key_string'  : b'_key_string',
    # history
    b'^Z'           : b'_history_undo',
    b'^Y'           : b'_history_redo',
    # selection
    b'^A'           : b'_select_key_all',
    # actions
    b'^B'           : b'_action_background',
    b'^C'           : b'_action_copy',
    b'^D'           : b'_action_interrupt',
    b'^E'           : b'_action_jump',
    b'^F'           : b'_action_find',
    b'^N'           : b'_action_insert',
    b'^P'           : b'_action_replace',
    b'^Q'           : b'_action_quit',
    b'^R'           : b'_action_reload',
    b'^S'           : b'_action_save',
    b'ALT_S'        : b'_action_save',
    b'^T'           : b'_action_transform',
    b'^V'           : b'_action_paste',
    b'^X'           : b'_action_cut',
    b'KEY_RESIZE'   : b'_action_resize',

    b'KEY_F(1)'     : b'_function_help',
    b'KEY_F(2)'     : b'_function_replace',
    b'KEY_F(3)'     : b'_function_search',
    b'KEY_F(14)'    : b'_function_replace_r',
    b'KEY_F(15)'    : b'_function_search_r',
} # translates key-inputs to pre-defined actions/methods

KEY_HOTKEYS      = set(v for v in UNIFY_HOTKEYS.values() if v.startswith(b'_key'     ))
INDENT_HOTKEYS   = set(v for v in UNIFY_HOTKEYS.values() if v.startswith(b'_indent'  ))
ACTION_HOTKEYS   = set(v for v in UNIFY_HOTKEYS.values() if v.startswith(b'_action'  ))
SCROLL_HOTKEYS   = set(v for v in UNIFY_HOTKEYS.values() if v.startswith(b'_scroll'  ))
MOVE_HOTKEYS     = set(v for v in UNIFY_HOTKEYS.values() if v.startswith(b'_move'    ))
HISTORY_HOTKEYS  = set(v for v in UNIFY_HOTKEYS.values() if v.startswith(b'_history' ))
SELECT_HOTKEYS   = set(v for v in UNIFY_HOTKEYS.values() if v.startswith(b'_select'  ))
FUNCTION_HOTKEYS = set(v for v in UNIFY_HOTKEYS.values() if v.startswith(b'_function'))

REVERSE_ACTION = {
    b'_key_dc'             : b'_key_string',
    b'_key_dl'             : b'_key_string',
    b'_key_backspace'      : b'_key_string',
    b'_key_ctl_backspace'  : b'_key_string',
    b'_key_string'         : b'_key_backspace',
    b'_indent_tab'         : b'_key_backspace',
    b'_indent_btab'        : b'_indent_tab',
    b'_key_enter'          : b'_key_backspace',
    b'_key_remove_chunk'   : b'_key_add_chunk',
    b'_key_add_chunk'      : b'_key_remove_chunk',
    b'_key_replace_search' : b'_key_replace_search_'
} # defines the counter action if no line was deleted

REVERSE_ACTION_MULTI_LINE = {
    b'_key_dc'             : b'_key_enter',
    b'_key_dl'             : b'_key_enter',
    b'_key_backspace'      : b'_key_enter',
    b'_key_ctl_backspace'  : b'_key_enter',
    b'_indent_tab'         : b'_indent_btab',
    b'_key_remove_chunk'   : b'_key_add_chunk',
    b'_key_add_chunk'      : b'_key_remove_chunk',
} # defines the counter action if a line was deleted

ACTION_STACKABLE = {
    b'_key_dc'             : [b'_key_dc'],
    b'_key_backspace'      : [b'_key_backspace'],
    b'_key_string'         : [b'_key_string'],
    b'_key_remove_chunk'   : [b'_key_add_chunk'],
    b'_key_add_chunk'      : [b'_key_remove_chunk'],
}
# these actions will be chained
# (e.g. when writing a word, the entire word should be undone/redone)


HEX_BYTE_KEYS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                 'A', 'B', 'C', 'D', 'E', 'F']


ESCAPE_MAP = {
    '\t': r"\t",
    '\n': r"\n",
    '\v': r"\v",
    '\f': r"\f",
    '\r': r"\r",
}
def frepr(string: str) -> str:
    """
    format repr
    """
    return ''.join(ESCAPE_MAP.get(c, c) for c in string)


class Position:
    """
    define a position in the text
    """
    def __init__(self, row: int, column: int) -> None:
        self.row = row
        self.col = column

    def get_pos(self) -> tuple:
        """
        return a tuple that defines the position.
        this makes comparison easier.

        Returns:
        (tuple):
            the position
        """
        return (self.row, self.col)

    def set_pos(self, new_pos: tuple) -> None:
        """
        setter for row and column of position

        Parameters:
        new_pos (tuple):
            the position
        """
        self.row, self.col = new_pos


class _Action:
    """
    _Action
    """
    def __init__(self, key_action: bytes, size_change: bool,
                 pre_cpos: tuple, post_cpos: tuple,
                 pre_spos: tuple, post_spos: tuple,
                 pre_selecting: bool, post_selecting: bool,
                 *action_text: str) -> None:
        """
        defines an action.

        Parameters:
        key_action (bytes):
            the action taken as defined by UNIFY_HOTKEYS
        size_change (bool)
            indicates if the size of the file changed because of this action
        pre_cpos (tuple):
            the cursor position before the action
        post_cpos (tuple):
            the cursor position after the action
        pre_spos (tuple):
            the selection position before the action
        post_spos (tuple):
            the selection position after the action
        pre_selecting (bool):
            the selecting indicator before the action
        post_selecting (bool):
            the selecting indicator after the action
        action_text* (str):
            the text added/removed by the action
        """
        self.key_action: bytes    = key_action
        self.size_change: bool    = size_change
        self.pre_cpos:  tuple     = pre_cpos
        self.post_cpos: tuple     = post_cpos
        self.pre_spos:  tuple     = pre_spos
        self.post_spos: tuple     = post_spos
        self.pre_selecting: bool  = pre_selecting
        self.post_selecting: bool = post_selecting
        self.action_text: tuple   = action_text

    def __str__(self) -> str:
        s_self = f"{self.key_action}|{repr(self.action_text)}|"
        s_self+= f"{self.size_change}{self.pre_cpos}{self.post_cpos}"
        return s_self

class History:
    """
    keeps track of editing history and provided
    undo/redo functionality.
    """
    def __init__(self, stack_size: int = 800) -> None:
        self.stack_size = max(stack_size, 1)

        # following stacks/lists will contain _Action objects.
        # each object needs ~300Bytes, meaning that both lists
        # together will be, at max, of the size ~600*stack_size (Bytes)
        # 500KB = 500_000B, 500_000/600 ~= 800
        self._stack_undo: list = []
        self._stack_redo: list = []

    def clear(self) -> None:
        """
        clear the history
        """
        self._stack_undo.clear()
        self._stack_redo.clear()

    def _add(self, action: _Action, stack_type: str = 'undo') -> None:
        """
        Add an action to the stack.

        Parameters:
        action (_Action):
            the action to append
        stack_type (str):
            defines the stack to use
        """
        if stack_type == 'undo':
            _stack = self._stack_undo
        elif stack_type == 'redo':
            _stack = self._stack_redo
        else:
            return

        if len(_stack) == self.stack_size:
            del _stack[0]
        _stack.append(action)

    def add(self, key_action: bytes, size_change: bool,
            pre_cpos: tuple, post_cpos: tuple,
            pre_spos: tuple, post_spos: tuple,
            pre_selecting: bool, post_selecting: bool,
            *action_text: str, stack_type: str = 'undo') -> None:
        """
        Add an action to the stack.

        Parameters:
        __init__ variables of _Action

        stack_type (str):
            defines the stack to use
        """
        if key_action not in REVERSE_ACTION and key_action not in REVERSE_ACTION_MULTI_LINE:
            return
        if not action_text or action_text[0] is None:
            # no edit has been made (e.g. invalid edit (backspace in top left))
            return

        if stack_type == 'undo':
            self._stack_redo.clear()

        action = _Action(key_action, size_change,
                         pre_cpos, post_cpos,
                         pre_spos, post_spos,
                         pre_selecting, post_selecting,
                         *action_text)
        self._add(action, stack_type)
        # print('Added', list(map(str, self._stack_undo)))
        # print('     ', list(map(str, self._stack_redo)))

    def _undo(self, editor: object, action: _Action) -> None:
        self._add(action, 'redo')
        if action.size_change:
            reverse_action = REVERSE_ACTION_MULTI_LINE.get(action.key_action)
        else:
            reverse_action = REVERSE_ACTION.get(action.key_action)
        if reverse_action is None:
            assert False, 'unreachable.'
        reverse_action_method = getattr(editor, reverse_action.decode(), lambda *_: None)
        editor.cpos.set_pos(action.post_cpos)
        editor.spos.set_pos(action.post_spos)
        editor.selecting = action.post_selecting
        reverse_action_method(*action.action_text)
        editor.cpos.set_pos(action.pre_cpos)
        editor.spos.set_pos(action.pre_spos)
        editor.selecting = action.pre_selecting

    def undo(self, editor: object) -> None:
        """
        Undo an action taken.

        Parameters:
        editor (Editor):
            the editor in use
        """
        try:
            action: _Action = self._stack_undo.pop()
        except IndexError:
            return

        self._undo(editor, action)
        is_space = action.action_text[0].isspace()
        while self._stack_undo:
            n_action: _Action = self._stack_undo.pop()
            if action.pre_cpos == n_action.post_cpos and \
                n_action.key_action in ACTION_STACKABLE.get(action.key_action, []) and \
                is_space == n_action.action_text[0].isspace():
                action = n_action
                self._undo(editor, action)
            else:
                self._stack_undo.append(n_action)
                break
        # print('Undo ', list(map(str, self._stack_undo)))
        # print('     ', list(map(str, self._stack_redo)))

    def _redo(self, editor: object, action: _Action) -> None:
        self._add(action, 'undo')
        reverse_action_method = getattr(editor, action.key_action.decode(), lambda *_: None)
        editor.cpos.set_pos(action.pre_cpos)
        editor.spos.set_pos(action.pre_spos)
        editor.selecting = action.pre_selecting
        reverse_action_method(*action.action_text)
        # neccessary because selecting can flip spos and cpos
        editor.cpos.set_pos(action.post_cpos)
        editor.spos.set_pos(action.post_spos)
        editor.selecting = action.post_selecting

    def redo(self, editor: object) -> None:
        """
        Redo an action taken.

        Parameters:
        editor (Editor):
            the editor in use
        """
        try:
            action: _Action = self._stack_redo.pop()
        except IndexError:
            return

        self._redo(editor, action)
        is_space = action.action_text[0].isspace()
        while self._stack_redo:
            n_action: _Action = self._stack_redo.pop()
            if action.post_cpos == n_action.pre_cpos and \
                action.key_action in ACTION_STACKABLE.get(n_action.key_action, []) and \
                is_space == n_action.action_text[0].isspace():
                action = n_action
                self._redo(editor, action)
            else:
                self._stack_redo.append(n_action)
                break
        # print('Redo ', list(map(str, self._stack_undo)))
        # print('     ', list(map(str, self._stack_redo)))
