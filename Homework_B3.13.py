# Экземпляр класса хранит в атрибуте "text" сформированый код html страницы и определяет вывод сформированной
# html страницы на экран или запись в файл "index.html"
class HTML:
    # Инициализация экземпляра класса с двумя атрибутами "text" и "output_to_f"
    def __init__ (self, output_to_f = True):
        self.output_to_f = output_to_f
        self.text = ""
    
    # Метор, выполняемый при входе в контекст экземпляра класса (возвращает сам экземпляр)
    def __enter__ (self):
        return self
    
    # Метод, выполняемый при выходе из контекста экземпляра класса. Предполагает вариативность: запись в файл
    # "index.html", который создается в директории исполняемого файла или вывод на экран. В качестве селектора
    # используется атрибут "output_to_f", имеющий тип bool. Значение по умолчанию True, которое предусматривает
    # запись html страницы в файл
    def __exit__ (self, type, value, traceback):
        if self.output_to_f:
            f = open("index.html", "w", encoding = "UTF-8")
            f.write(self.text)
            f.close
        else:
            print(self.text)
    
    # Метод определяющий логику формирования html страницы из результата обработки экземпляров классов TopLevelTag
    # и Tag. Hезультат храниться в атрибуте "text"
    def __add__ (self, other):
        self.text += other

# Класс верхнеуровневых тегов. В отличие от общего класса тегов не содержит текста и теги всегда парные
class TopLevelTag:

    # Инициализация экземпляра класса с четырмя атрибутами: "tag" - наименование тега, "klass" - указатель наличия
    # классов, "attributes" - сожержит классы тега и "children" - содержит вложенные теги
    def __init__ (self, tag, klass = None, **kwargs):    
        self.tag = tag
        self.klass = klass
        self.attributes = {}
        self.children = ""
        
        # При инициализации экземпляра класса при наличии классов, записывает классы в атрибут "attributes". Требует
        # строку в параметре klass
        if klass is not None:
            if " " in klass:
                self.attributes["class"] = " ".join(klass.split())
            else:
                self.attributes["class"] = klass

        # Получает значения атрибутов тегов из параментров переданных при создание экземпляра класса и сохраняет их
        # в атрибуте "attributes"
        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value

    # Метор, выполняемый при входе в контекст экземпляра класса (возвращает сам экземпляр)
    def __enter__ (self):
        return self
    
    # Метор, выполняемый при выходе из контекст экземпляра класса
    def __exit__ (self, type, value, traceback):
        pass
    
    # Метод формирования кода html для передачи в текстовом формате родительскому тегу или html-странице. Учитывает
    # наличие атрибутов тега и вложеных тегов
    def __str__ (self):
        if len(self.children) == 0:
            if len(self.attributes) == 0:
                return "<{tag}></{tag}>".format(
                    tag = self.tag,
                )
            else:
                attrs = []
                for attribute, value in self.attributes.items():
                    attrs.append('%s = "%s"' % (attribute, value))
                attrs = " ".join(attrs)
                return "<{tag} {attrs}></{tag}>".format(
                    tag = self.tag,
                    attrs = attrs 
                )
        else:
            if len(self.attributes) == 0:
                return "<{tag}>\n{child}\n</{tag}>".format(
                    tag = self.tag,
                    child = self.children
                )
            else:
                attrs = []
                for attribute, value in self.attributes.items():
                    attrs.append('%s = "%s"' % (attribute, value))
                attrs = " ".join(attrs)
                return "<{tag} {attrs}>\n{child}\n</{tag}>".format(
                    tag = self.tag,
                    attrs = attrs,
                    child = self.children 
                )
    
    # Метод, получающий код html вложенных тегов в текстовом виде и хранящий его в атрибуте "children" для
    # последующей передачи родительскому тегу или html-странице внутри себя
    def __add__ (self, other):
        self.children += other

# Общий класс тегов. Тег может быть парным/непарным и содержать текст внутри себя. Является потомком класса
# "TopLevelTag". Если тег непарный, то он не может иметь вложенных тегов
class Tag(TopLevelTag):

    # Инициализация экземпляра класса с шестью атрибутами: "tag" - наименование тега, "klass" - указатель наличия
    # классов, "attributes" - сожержит классы тега, "children" - содержит вложенные теги, "is_single" - флаг парного
    # тега и "text" - текстовое содержание тега
    def __init__ (self, tag, is_single = False, klass = None, **kwargs):    
        self.tag = tag
        self.klass = klass
        self.attributes = {}
        self.children = ""
        self.is_single = is_single
        self.text = ""
        
        # При инициализации экземпляра класса при наличии классов, записывает классы в атрибут "attributes". Требует
        # строку в параметре klass
        if klass is not None:
            if " " in klass:
                self.attributes["class"] = " ".join(klass.split())
            else:
                self.attributes["class"] = klass

        # Получает значения атрибутов тегов из параментров переданных при создание экземпляра класса и сохраняет их
        # в атрибуте "attributes"
        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value

    # Метод формирования кода html для передачи в текстовом формате родительскому тегу или html-странице. Учитывает
    # наличие атрибутов тега, вложеных тегов, текстовое содержимое тега и парность тега
    def __str__ (self):
        if self.is_single:
            if len(self.attributes) == 0:
                return "    <{tag}/>".format(
                    tag = self.tag,
                )
            else:
                attrs = []
                for attribute, value in self.attributes.items():
                    attrs.append('%s = "%s"' % (attribute, value))
                attrs = " ".join(attrs)
                return "    <{tag} {attrs}/>".format(
                    tag = self.tag,
                    attrs = attrs,
                )
        else:
            if len(self.children) == 0:
                if len(self.attributes) == 0:
                    return "    <{tag}>{text}</{tag}>".format(
                        tag = self.tag,
                        text = self.text
                    )
                else:
                    attrs = []
                    for attribute, value in self.attributes.items():
                        attrs.append('%s = "%s"' % (attribute, value))
                    attrs = " ".join(attrs)
                    return "    <{tag} {attrs}>{text}</{tag}>".format(
                        tag = self.tag,
                        attrs = attrs,
                        text = self.text
                    )
            else:
                if len(self.attributes) == 0:
                    return "    <{tag}>{text}\n{child}\n</{tag}>".format(
                        tag = self.tag,
                        child = self.children,
                        text = self.text
                    )
                else:
                    attrs = []
                    for attribute, value in self.attributes.items():
                        attrs.append('%s = "%s"' % (attribute, value))
                    attrs = " ".join(attrs)
                    return "    <{tag} {attrs}>{text}\n{child}\n</{tag}>".format(
                        tag = self.tag,
                        attrs = attrs,
                        child = self.children,
                        text = self.text
                    )

# Код эксплуатирующий созданные классы для формирования html-страницы из задания
if __name__ == "__main__":
    with HTML(output_to_f = True) as doc:
        with TopLevelTag("html") as html:
            with TopLevelTag("head") as head:
                with Tag("title") as title:
                    title.text = "hello"
                head + str(title)
            html + str(head)
            with TopLevelTag("body") as body:
                with Tag("h1", klass = "main-text") as h1:
                    h1.text = "Test"
                body + (str(h1) + "\n")
                with Tag("div", klass = "container container-fluid", id = "lead") as div:
                    with Tag("p") as p:
                        p.text = "another test"
                    div + ("    " + str(p) + "\n")
                    with Tag("img", is_single = True, src = "/icon.png", data_image = "responsive") as img:
                        pass
                    div + ("    " + str(img))
                body + str(div)
            html + ("\n" + str(body))
        doc + str(html)