            
class Html:
    class Web_Page:
        def __init__(self):
            self.code = ["<!DOCTYPE html>\n<html>\n"]
            self.indent_level = 1
            
        def __enter__(self):
            return self
            
        def __exit__(self, exc_type, exc, tb):
            self.code.append("</html>\n")

        class __TAGSCOPE__:
            def __enter__(self):
                attrs_str = ""
                if self.attrs:
                    attrs_str = " " + " ".join(['{}="{}"'.format(k, v) for k, v in self.attrs.items()])
                
                tabs = "\t" * self.page.indent_level
                self.page.code.append("{}<{}{}>\n".format(tabs, self.tag_name, attrs_str))
                
                self.page.indent_level += 1
                return self
                
            def __exit__(self, exc_type, exc, tb):
                self.page.indent_level -= 1
                
                tabs = "\t" * self.page.indent_level
                self.page.code.append("{}</{}>\n".format(tabs, self.tag_name))

        def __tags__(self, tag: str, **attributes):
            scope = self.__TAGSCOPE__()
            scope.page = self
            scope.tag_name = tag
            scope.attrs = attributes
            return scope
        
        def section(self, command: str, **attributes):
            return self.__tags__(command, **attributes)
        
        def inline(self, command: str, text: str, **attributes):
            attrs_str = ""
            if attributes:
                attrs_str = " " + " ".join(['{}="{}"'.format(k, v) for k, v in attributes.items()])
            
            tabs = "\t" * self.indent_level
            self.code.append("{}<{}{}>{}</{}>\n".format(tabs, command, attrs_str, text, command))

        def extract_html_code(self):
            return "".join(self.code)



if __name__ == "__main__":
    web = Html()
    
    with web.Web_Page() as page:
        with page.section("head"):
            page.inline("title", "Delus Automated Web")
            
        with page.section("body", class_name="dark"):
            page.inline("h1", "Welcome to My Dashboard")
            
            page.inline("img", "", src="logo.png", alt="Server Logo")
            page.inline("a", "Visit Kernel Website", href="https://...", target="_blank")
            
            with page.section("div"):
                page.inline("p", "Monitoring system active.")

    print(page.extract_html_code())
