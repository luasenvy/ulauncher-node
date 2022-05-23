import logging
import subprocess

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction

logger = logging.getLogger(__name__)

class NodeExtension(Extension):
  def __init__(self):
    super(NodeExtension, self).__init__()
    self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

    try:
      self.nodePath = subprocess.check_output(['which', 'node'], universal_newlines=True, stderr=subprocess.STDOUT).strip()
    except subprocess.CalledProcessError as errorMessage:
      self.nodePath = None
      self.nodePathErrorMessage = '\'node\' command not found. please install nodejs or make sure add PATH in system environment.'
      logger.error(self.nodePathErrorMessage)

class KeywordQueryEventListener(EventListener):
  def on_event(self, event, extension):
    items = []
    expression = event.get_argument()

    try:
      if None == extension.nodePath:
        items.append(ExtensionResultItem(icon='images/icon.png',
          name=extension.nodePathErrorMessage,
          description='\'node\' command is not found.',
          on_enter=CopyToClipboardAction(extension.nodePathErrorMessage)
        ))
        return RenderResultListAction(items)

      if None == expression:
        items.append(ExtensionResultItem(icon='images/icon.png',
          name='Node: there is no code.',
          description='please input script code.',
          on_enter=None
        ))
        return RenderResultListAction(items)

      result = subprocess.check_output([extension.nodePath, '-p', expression], universal_newlines=True, stderr=subprocess.STDOUT)

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
