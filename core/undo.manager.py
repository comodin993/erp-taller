class UndoManager:

    def __init__(self):
        self.stack = []

    def push(self, action):
        self.stack.append(action)

    def undo(self):
        if not self.stack:
            return

        action = self.stack.pop()
        action()