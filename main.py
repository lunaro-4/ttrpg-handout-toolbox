from template_handler import TemplateHandler


def main():


    th = TemplateHandler()
    soup = th.soup
    components_value = soup.new_tag("p")
    components_value.string = "123"
    th.components.append(components_value)

    th.render()


    # soup.b



if __name__ == "__main__":
    main()

