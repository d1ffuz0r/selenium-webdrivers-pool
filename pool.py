#!/usr/bin/env python


class WebPool(object):
    def __init__(self):
        self.browsers = {}
        self.result = {}
        self.actions = {}
        self.ignored = ('send_keys', 'get')

    def start(self):
        for name, browser in self.browsers.items():
            try:
                b = browser()
                self.browsers[name] = b
                self.result[name] = b
            except:
                self.result[name] = browser
        return self.result

    def stop(self):
        for name, browser in self.browsers.items():
            try:
                browser.quit()
            finally:
                del self.result[name]

    def action(self, action, arg=None):
        for name, browser in self.browsers.items():
            try:
                if not self.result[name] or action.startswith('find_'):
                    self.result[name] = getattr(browser, action)(arg)
                elif not arg:
                    self.result[name] = getattr(self.result[name], action)()
                elif action in self.ignored:
                    getattr(self.result[name], action)(arg)
                else:
                    self.result[name] = getattr(self.result[name], action)(arg)
            except:
                pass
        return self.result
