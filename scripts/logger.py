class MyLogger(object):
        def __init__(self):
            self.debug_msg = None
            self.warning_msg = None
            self.error_msg = None
            
        def debug(self, msg):
            self.debug_msg = msg

        def warning(self, msg):
            self.warning_msg = msg

        def error(self, msg):
            self.error_msg = msg
            
        def get_debug_msg(self):
            return self.debug_msg
        
        def get_warning_msg(self):
            return self.warning_msg
        
        def get_error_msg(self):
            return self.error_msg
        
        def get_all_msg(self):
            return {'debug': self.debug_msg, 'warning':self.warning_msg, 'error': self.error_msg}
        
        def reset(self):
            self.debug_msg = None
            self.warning_msg = None
            self.error_msg = None
