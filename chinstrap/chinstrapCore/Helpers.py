import os
import sys
import time
import shutil
import pytezos
from halo import Halo
from functools import wraps
from prompt_toolkit import HTML
from prompt_toolkit import prompt
from prompt_toolkit import print_formatted_text
from typing import List, Optional, Tuple, Union
from prompt_toolkit.application import Application, get_app
from prompt_toolkit.filters import IsDone
from prompt_toolkit.formatted_text import AnyFormattedText
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.dimension import Dimension
from prompt_toolkit.layout.containers import ConditionalContainer, HSplit
from prompt_toolkit.mouse_events import MouseEventType
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts import yes_no_dialog
from prompt_toolkit.shortcuts import print_container
from prompt_toolkit.widgets import Frame, TextArea, Box

OptionValue = Optional[AnyFormattedText]
Option = Union[
	AnyFormattedText,  # name value is same
	Tuple[AnyFormattedText, OptionValue]  # (name, value)
]
IndexedOption = Tuple[
	int,  # index
	AnyFormattedText,  # name
	OptionValue
]

def welcome_banner():
	colors = ['ansigreen', 'ansired', 'ansiyellow']

	banner =HTML("""
      _     _           _                   
  ___| |__ (_)_ __  ___| |_ _ __ __ _ _ __  
 / __| '_ \| | '_ \/ __| __| '__/ _` | '_ \ 
| (__| | | | | | | \__ \ |_| | | (_| | |_) |
 \___|_| |_|_|_| |_|___/\__|_|  \__,_| .__/ 
                                     |_|    
""")

	print_formatted_text(banner)                              
                                      

def debug(msg):
	m = HTML(f"<ansiyellow>{msg}</ansiyellow>\n")
	print_formatted_text(m)

def success(msg):
	m = HTML(f"<ansigreen>{msg}</ansigreen>\n")
	print_formatted_text(m)

def fatal(msg):
	m = HTML(f"<ansired>{msg}</ansired>")
	print_formatted_text(m)
	hexit()

def hexit():
	print_formatted_text(HTML(f"Thanks for using <b><ansired>Chinstrap</ansired></b>! Happy Hacking 🙏🏻"))
	sys.exit()

def promptOverwrite(dir):
	msg = HTML(f"<i><b>{dir}</b></i> already exists in this directory. Should I <b>Overwrite?: </b>")
	p = SelectionPrompt()
	inp = p.prompt(msg, options=['y', 'n'])
	if inp == 'y':
		return True
	return False

def rmdir(path):
	shutil.rmtree(path, ignore_errors=True)

def mkdir(path):
	try:
		os.mkdir(path)
	except Exception as e:
		pass

def copyFile(src, dest):
	shutil.copyfile(src, dest)

class SelectionControl(FormattedTextControl):
	def __init__(
			self,
			options: List[Option],
			**kwargs
	) -> None:
		self.options = self._index_options(options)
		self.answered = False
		self.selected_option_index = 0
		super().__init__(**kwargs)

	@property
	def selected_option(self) -> IndexedOption:
		return self.options[self.selected_option_index]

	@property
	def options_count(self) -> int:
		return len(self.options)

	def _index_options(self, options) -> List[IndexedOption]:
		indexed_options = []
		for idx, opt in enumerate(options):
			if isinstance(opt, str):
				indexed_options.append((idx, opt, opt))
			if isinstance(opt, tuple):
				if len(opt) != 2:
					raise ValueError(f'invalid tuple option: {opt}.')
				indexed_options.append((idx, *opt))

		return indexed_options

	def _select_option(self, index):

		def handler(mouse_event):
			if mouse_event.event_type != MouseEventType.MOUSE_DOWN:
				raise NotImplemented

			# bind option with this index to mouse event
			self.selected_option_index = index
			self.answered = True
			get_app().exit(result=self.selected_option)

		return handler

	def format_option(
			self,
			option: IndexedOption,
			*,
			selected_style_class: str = '',
			selected_prefix_char: str = '>',
			indent: int = 1
	):
		option_prefix: AnyFormattedText = ' ' * indent
		idx, name, value = option
		if self.selected_option_index == idx:
			option_prefix = selected_prefix_char + option_prefix
			return selected_style_class, f'{option_prefix}{name} ', self._select_option(idx)

		option_prefix += ' '
		return '', f'{option_prefix}{name} ', self._select_option(idx)

class SelectionControlList(FormattedTextControl):
    def __init__(
            self,
            options: List[Option],
            **kwargs
    ) -> None:
        self.options = self._index_options(options)
        self.answered = False
        self.selected_option_index = 0
        super().__init__(**kwargs)

    @property
    def selected_option(self) -> IndexedOption:
        return self.options[self.selected_option_index]

    @property
    def options_count(self) -> int:
        return len(self.options)

    def _index_options(self, options) -> List[IndexedOption]:
        """
        Convert Option to IndexedOption
        """
        indexed_options = []
        for idx, opt in enumerate(options):
            if isinstance(opt, str):
                indexed_options.append((idx, opt, opt))
            if isinstance(opt, tuple):
                if len(opt) != 2:
                    raise ValueError(f'invalid tuple option: {opt}.')
                indexed_options.append((idx, *opt))

        return indexed_options

    def _select_option(self, index):

        def handler(mouse_event):
            if mouse_event.event_type != MouseEventType.MOUSE_DOWN:
                raise NotImplemented

            # bind option with this index to mouse event
            self.selected_option_index = index
            self.answered = True
            get_app().exit(result=self.selected_option)

        return handler

    def format_option(
            self,
            option: IndexedOption,
            *,
            selected_style_class: str = '',
            selected_prefix_char: str = '>',
            indent: int = 1
    ):
        option_prefix: AnyFormattedText = ' ' * indent
        idx, name, value = option
        if self.selected_option_index == idx:
            option_prefix = selected_prefix_char + option_prefix
            return selected_style_class, f'{option_prefix}{name}\n', self._select_option(idx)

        option_prefix += ' '
        return '', f'{option_prefix}{name}\n', self._select_option(idx)


# https://github.com/prompt-toolkit/python-prompt-toolkit/issues/1071#issuecomment-731915746
class SelectionPrompt:
	def __init__(
			self,
			message: AnyFormattedText = "",
			*,
			options: List[Option] = None,
			sideBySide = True
	) -> None:
		self.message = message
		self.options = options
		self.sideBySide = sideBySide
		self.control = None
		self.layout = None
		self.key_bindings = None
		self.app = None

	def _create_layout(self) -> Layout:
		def get_option_text():
			return [
				self.control.format_option(
					opt, selected_style_class='class:reverse'
				) for opt in self.control.options
			]

		layout = HSplit([
			Window(
				height=Dimension.exact(1),
				content=FormattedTextControl(
					lambda: self.message,
					show_cursor=False
				),
			),
			Window(
				# height=Dimension.exact(self.control.options_count),
				content=FormattedTextControl(get_option_text)
			),
			ConditionalContainer(
				Window(self.control),
				filter=~IsDone()
			)
		]
		)
		return Layout(layout)

	def _create_key_bindings(self) -> KeyBindings:
		"""
		Create `KeyBindings` for this prompt
		"""
		control = self.control
		kb = KeyBindings()

		@kb.add('c-q', eager=True)
		@kb.add('c-c', eager=True)
		def _(event):
			raise KeyboardInterrupt()

		@kb.add('right', eager=True)
		def move_cursor_right(event):
			control.selected_option_index = (control.selected_option_index + 1) % control.options_count

		@kb.add('left', eager=True)
		def move_cursor_left(event):
			control.selected_option_index = (control.selected_option_index - 1) % control.options_count

		@kb.add('up', eager=True)
		def move_cursor_up(event):
			control.selected_option_index = (control.selected_option_index + 1) % control.options_count

		@kb.add('down', eager=True)
		def move_cursor_down(event):
			control.selected_option_index = (control.selected_option_index + 1) % control.options_count

		@kb.add('left', eager=True)
		def move_cursor_left(event):
			control.selected_option_index = (control.selected_option_index - 1) % control.options_count

		@kb.add('enter', eager=True)
		def set_answer(event):
			control.answered = True
			_, _, selected_option_value = control.selected_option
			event.app.exit(result=selected_option_value)

		return kb

	def _create_application(self) -> Application:
		style = Style.from_dict(
			{
				"status": "reverse",
			}
		)
		app = Application(
			layout=self.layout,
			key_bindings=self.key_bindings,
			style=style,
			full_screen=False
		)
		return app

	def prompt(
			self,
			message: Optional[AnyFormattedText] = None,
			*,
			options: List[Option]
	):
		# all arguments are overwritten the init arguments in SelectionPrompt.
		if message is not None:
			self.message = message
		if options is not None:
			self.options = options

		if self.app is None:
			if self.sideBySide:
				self.control = SelectionControl(self.options)
			else:
				self.control = SelectionControlList(self.options)
			self.layout = self._create_layout()
			self.key_bindings = self._create_key_bindings()
			self.app = self._create_application()

		return self.app.run()


def confirmChinstrapProjectDirectory():
	if not os.path.exists('./chinstrap_config.yaml'):
		fatal("Please run the command from inside your project's root folder")


class Dict2Object(object):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
               setattr(self, a, [Dict2Object(x) if isinstance(x, dict) else x for x in b])
            else:
               setattr(self, a, Dict2Object(b) if isinstance(b, dict) else b)

def convertYamlToObject(d):
	top = type('Object', (object,), d)
	seqs = tuple, list, set, frozenset
	for i, j in d.items():
		if isinstance(j, dict):
			setattr(top, i, convertYamlToObject(j))
		elif isinstance(j, seqs):
			setattr(top, i, 
				type(j)(convertYamlToObject(sj) if isinstance(sj, dict) else sj for sj in j))
		else:
			setattr(top, i, j)
	return top

def handleException():
    def catch(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                debug(e)
        return wrapper
    return catch

def waitForBaking(ophash, pytezoscli):
	spinner = Halo(text='Baking...', spinner='dots')
	spinner.start()
	while 1:
		try:
			opg = pytezoscli.shell.blocks[-5:].find_operation(ophash)
			break
		except StopIteration:
			continue
		except pytezos.rpc.node.RpcError:
			debug('rpcerror: sleeping for sometime!')
			time.sleep(5)
			continue
		except Exception as e:
			fatal(e)
	
	spinner.stop_and_persist(symbol='✓'.encode('utf-8'), text=f"Baking successful!")
	return opg
