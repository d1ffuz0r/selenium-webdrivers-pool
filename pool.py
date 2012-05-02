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
            except:
                pass
            finally:
                del self.result[name]

    def action(self, action, arg):
        for name, browser in self.browsers.items():
            try:
                if not self.result[name]:
                    self.result[name] = getattr(browser, action)(arg)
                elif action in self.ignored:
                    getattr(self.result[name], action)(arg)
                else:
                    self.result[name] = getattr(self.result[name], action)(arg)
            except:
                pass
        return self.result
