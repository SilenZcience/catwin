from functools import lru_cache, reduce
from heapq import nlargest

from cat_win.const.ArgConstants import *
from cat_win.util.File import File


class Holder():
    def __init__(self) -> None:
        self.files: list = []  # all files, including tmp-file from stdin
        self._inner_files: list = []
        self.args: list = []  # list of all used parameters: format [[id, param]]
        self.args_id: list = [False] * (HIGHEST_ARG_ID + 1)
        self.temp_file_stdin = None  # if stdin is used, this temp_file will contain the stdin-input
        self.temp_file_echo = None  # if ARGS_ECHO is used, this temp_file will contain the following parameters
        self.reversed = False
        
        # the amount of chars neccessary to display the last file
        self.fileNumberPlaceHolder = 0
        # the sum of all lines of all files
        self.allFilesLinesSum = 0
        # the sum of lines for each file individually
        self.allFilesLines = {}
        # the amount of chars neccessary to display the last line (breaks on base64 decoding)
        self.fileLineNumberPlaceHolder = 0
        # the amount of chars neccessary to display the longest line within all files (breaks on base64 decoding)
        self.fileLineLengthPlaceHolder = 0

        self.clipBoard = ''
    
    def _getFileDisplayName(self, file: str) -> str:
        """
        return the display name of a file. Expects self.temp_file_stdin
        and self.temp_file_echo to be set already.
        
        Parameters_
        file (str):
            a path of a file
            
        Returns:
        (str):
            the display name for the file. Either the path itself
            or a special identifier von stdin or echo inputs
        """
        if file == self.temp_file_stdin:
            return '<STDIN>'
        elif file == self.temp_file_echo:
            return '<ECHO>'
        return file
    
    def setFiles(self, files: list) -> None:
        self.files = [File(path, self._getFileDisplayName(path)) for path in files]
        self._inner_files = files[:]

    def setArgs(self, args: list) -> None:
        self.args = reduce(lambda l, x: l + [x] if x not in l else l, args, [])
        for id, _ in self.args:
            self.args_id[id] = True
        if self.args_id[ARGS_B64E]:
            self.args_id[ARGS_NOCOL] = True
            # prefix will be deleted anyway
            self.args_id[ARGS_LLENGTH] = False
            self.args_id[ARGS_NUMBER] = False
        self.reversed = self.args_id[ARGS_REVERSE]
        
    def addArgs(self, args: list) -> None:
        self.args_id = [False] * (HIGHEST_ARG_ID + 1)
        self.setArgs(self.args + args)
        
    def deleteArgs(self, args: list) -> None:
        self.args_id = [False] * (HIGHEST_ARG_ID + 1)
        self.setArgs([arg for arg in self.args if not arg in args])

    def setTempFileStdIn(self, file: str) -> None:
        self.temp_file_stdin = file
        
    def setTempFileEcho(self, file: str) -> None:
        self.temp_file_echo = file
    
    def __calcFileNumberPlaceHolder__(self) -> None:
        self.fileNumberPlaceHolder = len(str(len(self.files)))

    def __count_generator__(self, reader):
        """
        Parameters:
        reader (method):
            the method to read from
        
        Yields:
        b (bytes):
            the bytes in chunks read from the reader
        """
        b = reader(1024 * 1024)
        while b:
            yield b
            b = reader(1024 * 1024)

    @lru_cache(maxsize=10)
    def __getFileLinesSum__(self, file: str) -> int:
        with open(file, 'rb') as fp:
            c_generator = self.__count_generator__(fp.raw.read)
            linesSum = sum(buffer.count(b'\n') for buffer in c_generator) + 1
        return linesSum

    def __calcPlaceHolder__(self) -> None:
        fileLines = []
        for file in self._inner_files:
            fileLineSum = self.__getFileLinesSum__(file)
            fileLines.append(fileLineSum)
            self.allFilesLines[file] = fileLineSum
        self.allFilesLinesSum = sum(fileLines)
        self.fileLineNumberPlaceHolder = len(str(max(fileLines)))

    @lru_cache(maxsize=10)
    def __calcMaxLineLength__(self, file: str) -> int:
        """
        Calculate self.fileLineLengthPlaceHolder for a single file.
        
        Parameters:
        file (str):
            a string representation of a file (-path)
            
        Returns:
        (int):
            the length of the placeholder to represent
            the longest line within the file
        """
        heap = []
        lines = []
        with open(file, 'rb') as fp:
            lines = fp.readlines()
        
        heap = nlargest(1, lines, len)
        if len(heap) == 0:
            return 0
        # also check the longest line against the last line because
        # the lines still contain (\r)\n, except the last line does not
        longest_line_len = len(heap[0][:-1].rstrip(b'\n').rstrip(b'\r'))
        last_line_len = len(lines[-1].rstrip(b'\n').rstrip(b'\r'))
        
        return len(str(max(longest_line_len, last_line_len)))

    def __calcFileLineLengthPlaceHolder__(self) -> None:
        self.fileLineLengthPlaceHolder = max(self.__calcMaxLineLength__(file)
                                             for file in self._inner_files)
        
    def setDecodingTempFiles(self, temp_files: list) -> None:
        self._inner_files = temp_files[:]

    def generateValues(self, encoding: str) -> None:
        self.__calcFileNumberPlaceHolder__()
        if self.args_id[ARGS_B64D]:
            from cat_win.util.Base64 import _decodeBase64
            for i, file in enumerate(self.files):
                with open(file.path, 'rb') as fp:
                    with open(self._inner_files[i], 'wb') as f:
                        f.write(_decodeBase64(fp.read().decode(encoding)))
        self.__calcPlaceHolder__()
        self.__calcFileLineLengthPlaceHolder__()
