    def send_cmd(self, action, arguments, timeout = 5):
        ret = None
        try:
            datastr = json.dumps({
                'action': action,
                'arguments': arguments
            }, ensure_ascii=False)
            print "req: %s\n\n" % (datastr)
            self._sock.sendall("%s\r\n\r\n%s" % (len(datastr), datastr))
            print "Sendall finished!!!"
            time.sleep(3)
            self._sock.settimeout(timeout)
            ret = self.getret()
        except Exception as e:
            print "send_cmd exception:", e
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print traceback.format_exception(exc_type, exc_value, exc_traceback)
            pass
        return ret    