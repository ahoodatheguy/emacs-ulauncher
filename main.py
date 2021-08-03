import json
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
import os
from time import sleep

class DemoExtension(Extension):

	def __init__(self):
		super(DemoExtension, self).__init__()
		self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

	def on_event(self, event, extension):
		items = []
		daemons = os.listdir('/run/user/1000/emacs/')

		search_term = event.get_argument()
		
		for daemon in daemons:
				items.append(ExtensionResultItem(icon='images/icon.png',
												 name=daemon,
												 description=f'Open {daemon}',
												 on_enter=RunScriptAction(f'emacsclient -c -s {search_term}')))
		if search_term not in daemons:
			items.append(ExtensionResultItem(icon='images/icon.png',
												name=search_term,
												description=f'Create {search_term}',
												on_enter=RunScriptAction(f'emacs --daemon={search_term}; emacsclient -c -s {search_term}')))


		return RenderResultListAction(items)




if __name__ == '__main__':
	DemoExtension().run()
