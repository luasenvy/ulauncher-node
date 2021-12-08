import subprocess

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction

class NodeExtension(Extension):

  def __init__(self):
    super(NodeExtension, self).__init__()
    self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

class KeywordQueryEventListener(EventListener):

  def on_event(self, event, extension):
    items = []
    expression = event.get_argument()
    try:
      result = subprocess.check_output(['node', '-p', expression], universal_newlines=True, stderr=subprocess.STDOUT)

      items.append(ExtensionResultItem(icon='images/icon.png',
        name=result,
        description='Press \'enter\' to copy to clipboard.',
        on_enter=CopyToClipboardAction(result)
      ))
    except subprocess.CalledProcessError as errorMessage:
      items.append(ExtensionResultItem(icon='images/icon.png',
        name='Node: %s' % errorMessage.output,
        description='Expression has Error.',
        on_enter=CopyToClipboardAction(errorMessage.output)
      ))
    return RenderResultListAction(items)

if __name__ == '__main__':
   NodeExtension().run()
