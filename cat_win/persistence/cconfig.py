"""
cconfig
"""

import configparser
import os
import sys

from cat_win.const.colorconstants import ColorOptions, CKW


class CConfig:
    """
    manages the color configuration. Displays the user interface,
    allows for reading and writing the config file.
    """
    default_dic = {
        CKW.NUMBER: ColorOptions.Fore['GREEN'],
        CKW.LINE_LENGTH: ColorOptions.Fore['LIGHTBLUE'],
        CKW.FILE_PREFIX: ColorOptions.Fore['LIGHTMAGENTA'],
        CKW.ENDS: ColorOptions.Back['YELLOW'],
        CKW.CHARS: ColorOptions.Fore['YELLOW'],
        CKW.CONVERSION: ColorOptions.Fore['CYAN'],
        CKW.EVALUATION: ColorOptions.Fore['BLUE'],
        CKW.REPLACE: ColorOptions.Fore['YELLOW'],
        CKW.FOUND: ColorOptions.Fore['RED'],
        CKW.FOUND_MESSAGE: ColorOptions.Fore['MAGENTA'],
        CKW.MATCHED: ColorOptions.Back['CYAN'],
        CKW.MATCHED_MESSAGE: ColorOptions.Fore['LIGHTCYAN'],
        CKW.CHECKSUM: ColorOptions.Fore['CYAN'],
        CKW.SUMMARY: ColorOptions.Fore['CYAN'],
        CKW.ATTRIB_POSITIVE: ColorOptions.Fore['LIGHTGREEN'],
        CKW.ATTRIB_NEGATIVE: ColorOptions.Fore['LIGHTRED'],
        CKW.ATTRIB: ColorOptions.Fore['CYAN'],
        CKW.RAWVIEWER: ColorOptions.Fore['LIGHTBLACK'],
        CKW.MESSAGE_INFORMATION: ColorOptions.Fore['LIGHTBLACK'],
        CKW.MESSAGE_IMPORTANT: ColorOptions.Fore['YELLOW'],
        CKW.MESSAGE_WARNING: ColorOptions.Fore['RED'],
        CKW.RESET_ALL: ColorOptions.Style['RESET'],
        CKW.RESET_FOUND: ColorOptions.Fore['RESET'],
        CKW.RESET_MATCHED: ColorOptions.Back['RESET'],
    }
    elements = [k for k in default_dic.keys() if 'reset' not in k]

    def __init__(self, working_dir: str) -> None:
        """
        Initialise the CConfig() object to load and save
        the color configs.
        
        Parameters:
        working_dir (str):
            the working directory path of the package
        """
        self.working_dir = working_dir
        self.config_file = os.path.join(self.working_dir, 'cat.config')

        self.exclusive_definitions = {'Fore': [CKW.FOUND],  # can only be Foreground
                                      'Back': [CKW.MATCHED]}  # can only be Background
        self.config_parser = configparser.ConfigParser()
        self.color_dic = {}

    def load_config(self) -> dict:
        """
        Load the Color Configuration from the config file.
        
        Returns:
        color_dic (dict):
            a dictionary translating from CKW-keywords to ANSI-Colorcodes
        On Error: Return the default color config
        """
        try:
            self.config_parser.read(self.config_file, encoding='utf-8')
            config_colors = self.config_parser['COLORS']
            for element in self.elements:
                try:
                    color_type, color = config_colors[element].split('.')
                    self.color_dic[element] = (
                        ColorOptions.Fore[color] if color_type == 'Fore'
                        else ColorOptions.Back[color]
                        )
                except KeyError:
                    self.color_dic[element] = self.default_dic[element]
        except KeyError:
            self.config_parser['COLORS'] = {}
            # If an error occures we simply use the default colors
            self.color_dic = self.default_dic.copy()

        # The Reset Codes should always be the same
        self.color_dic[CKW.RESET_ALL] = ColorOptions.Style['RESET']
        self.color_dic[CKW.RESET_FOUND] = ColorOptions.Fore['RESET']
        self.color_dic[CKW.RESET_MATCHED] = ColorOptions.Back['RESET']

        return self.color_dic

    def _print_get_all_available_colors(self) -> list:
        """
        prints all available color options to choose from.
        
        Returns:
        options (list):
            the same list containing all available colors.
        """
        print('Here is a list of all available color options you may choose:')

        fore_options = list(ColorOptions.Fore.items())
        fore_options = [(k, v) for k, v in fore_options if k != 'RESET']
        back_options = list(ColorOptions.Back.items())
        back_options = [(k, v) for k, v in back_options if k != 'RESET']

        h_width, _ = os.get_terminal_size()
        index_offset = max(len(str(len(fore_options) + len(back_options))),
                           len(str(len(self.elements))))

        longest_char_count = max(max(map(len, fore_options+back_options))+5,
                                 max(map(len, self.elements)))
        column_width = index_offset+4 + longest_char_count
        columns = max(h_width // column_width, 1)
        element_offset = longest_char_count + max(
            (h_width - columns * column_width) // columns,
            1
        )

        config_menu = ''
        options = []

        for index, fore_option in enumerate(fore_options):
            key, value = fore_option
            f_key = f"Fore.{key}"
            config_menu += f"{index+1: <{index_offset}}: {value}"
            if key == 'BLACK':
                config_menu += f"{ColorOptions.Back['LIGHTBLACK']}"
                config_menu += f"{f_key}{ColorOptions.Style['RESET']}"
                config_menu += f"{' ' * (element_offset-len(f_key))} "
            else:
                config_menu += f"{f_key: <{element_offset}}"
                config_menu += f"{ColorOptions.Style['RESET']} "
            if index % columns == columns-1:
                config_menu += '\n'
            options.append('Fore.' + key)
        config_menu += '\n'
        for index, back_option in enumerate(back_options):
            key, value = back_option
            b_key = f"Back.{key}"
            config_menu += f"{len(fore_options)+index+1: <{index_offset}}: {value}"
            if key not in ['NONE', 'BLACK']:
                config_menu += f"{ColorOptions.Fore['BLACK']}"
            config_menu += f"{b_key: <{element_offset}}"
            config_menu += f"{ColorOptions.Style['RESET']} "
            if index % columns == columns-1:
                config_menu += '\n'
            options.append('Back.' + key)
        config_menu += '\n'

        print(config_menu)
        return options

    def _print_all_available_elements(self) -> None:
        """
        print all available elements that can be changed.
        """
        print('Here is a list of all available elements you may change:')

        h_width, _ = os.get_terminal_size()
        index_offset = len(str(len(self.elements)))

        longest_char_count = max(map(len, self.elements))
        column_width = index_offset+4 + longest_char_count
        columns = max(h_width // column_width, 1)
        element_offset = longest_char_count + max(
            (h_width - columns * column_width) // columns,
            1
        )
        config_menu = ''

        for index, element in enumerate(self.elements):
            config_menu += f"{index+1: <{index_offset}}: {self.color_dic[element]}"
            if self.color_dic[element] == ColorOptions.Fore['BLACK']:
                config_menu += f"{ColorOptions.Back['LIGHTBLACK']}"
                config_menu += f"{element}{ColorOptions.Style['RESET']}"
                config_menu += f"{' ' * (element_offset-len(element))} "
            else:
                if self.color_dic[element] in [c for k,c in ColorOptions.Back.items() if k not in ['NONE', 'BLACK']]:
                    config_menu += f"{ColorOptions.Fore['BLACK']}"
                config_menu += f"{element: <{element_offset}}"
                config_menu += f"{ColorOptions.Style['RESET']} "
            if index % columns == columns-1:
                config_menu += '\n'

        print(config_menu)

    def save_config(self) -> None:
        """
        Guide the User through the configuration options and save the changes.
        Assume, that the current config is already loaded/
        the method load_config() was already called.
        """
        self._print_all_available_elements()
        keyword = ''
        while keyword not in self.elements:
            if keyword != '':
                print(f"Something went wrong. Unknown keyword '{keyword}'")
            try:
                keyword = input('Input name or id of the element to change: ')
            except EOFError:
                print('\nAborting due to End-of-File character...', file=sys.stderr)
                return
            if keyword.isdigit():
                keyword = self.elements[int(keyword)-1] if (
                    0 < int(keyword) <= len(self.elements)) else keyword
        print('Successfully selected element ', end='')
        print(f"'{self.color_dic[keyword]}{keyword}{ColorOptions.Style['RESET']}'.")

        color_options = self._print_get_all_available_colors()
        color = ''
        while color not in color_options:
            if color != '':
                print(f"Something went wrong. Unknown option '{color}'.")
            try:
                color = input('Input new color: ')
            except EOFError:
                print('\nAborting due to End-of-File character...', file=sys.stderr)
                return
            if color.isdigit():
                color = color_options[int(color)-1] if (
                    0 < int(color) <= len(color_options)) else color

        if keyword in self.exclusive_definitions['Fore'] and color.startswith('Back'):
            print(f"An Error occured: '{keyword}' can only be of style 'Fore'", file=sys.stderr)
            return
        if keyword in self.exclusive_definitions['Back'] and color.startswith('Fore'):
            print(f"An Error occured: '{keyword}' can only be of style 'Back'", file=sys.stderr)
            return

        color_split = color.split('.')
        print('Successfully selected element ', end='')
        print(f"'{getattr(ColorOptions, color_split[0])[color_split[1]]}", end='')
        print(f"{color}{ColorOptions.Style['RESET']}'.")

        self.config_parser['COLORS'][keyword] = color
        try:
            with open(self.config_file, 'w', encoding='utf-8') as conf:
                self.config_parser.write(conf)
            print(f"Successfully updated config file:\n\t{self.config_file}")
        except OSError:
            print(f"Could not write to config file:\n\t{self.config_file}", file=sys.stderr)
