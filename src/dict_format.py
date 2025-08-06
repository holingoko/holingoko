import traceback

from src import dict_re


class Formatter:
    def __init__(self, entry_format, tag_name_to_tag_values_format):
        self.parsed_entry_format = self.parse_entry_format(entry_format)
        self.tag_name_to_parsed_tag_values_format = {
            tag_name: self.parse_tag_values_format(tag_values_format)
            for tag_name, tag_values_format in tag_name_to_tag_values_format.items()
        }

    @classmethod
    def check_entry_format(cls, in_):
        try:
            parsed_entry_format = cls.parse_entry_format(in_)
            conditionals = parsed_entry_format[1]
            tag_sets = []
            tags = set()
            for conditional in conditionals:
                tag_set = set()
                for expression in conditional:
                    tag_set.update(expression[1])
                tag_sets.append(tag_set)
                tags.update(tag_set)
            tag_name_to_tag_values_format = {
                tag_name: "{}" for tag_name in tags
            }
            formatter = cls(in_, tag_name_to_tag_values_format)
            for tag_set in tag_sets:
                tag_values = {tag_name: "tag_value" for tag_name in tag_set}
                formatter.format(tag_values)
            return True
        except:
            print(traceback.format_exc())
            return False

    @classmethod
    def check_tag_values_format(cls, in_):
        try:
            tag_name = "tag_name"
            formatter = cls(f"{{{tag_name}}}", {tag_name: in_})
            max_possible_num_values = in_.count("{}")
            for num_values in range(max_possible_num_values):
                tag_values = {tag_name: [f"{i}" for i in range(num_values)]}
                formatter.format(tag_values)
            return True
        except:
            print(traceback.format_exc())
            return False

    @staticmethod
    def parse_entry_format(in_):
        in_ = dict_re.replace_non_tag_curly_braces(in_)
        return dict_re.parse(in_)

    @staticmethod
    def parse_tag_values_format(in_):
        in_ = dict_re.replace_non_tag_curly_braces(in_)
        in_, (order_reversed,) = dict_re.parse_option_tags(in_)
        return [
            (format_string, order_reversed)
            for format_string, _ in dict_re.parse_conditional(in_)
        ]

    @classmethod
    def entry_format_tags(cls, in_):
        tags = set()
        conditionals = cls.parse_entry_format(in_)[1]
        for conditional in conditionals:
            for expression in conditional:
                tags.update(expression[1])
        return tags

    @classmethod
    def format_multiple_values(cls, values, multiple_values_format):
        conditionals = cls.parse_tag_values_format(multiple_values_format)
        num_values = len(values)
        for format_string, order_reversed in conditionals:
            expanded_format_string = (
                dict_re.expand_tag_values_format_expression(
                    format_string,
                    num_values,
                )
            )
            if expanded_format_string:
                if order_reversed:
                    tag_values_ = reversed(values)
                else:
                    tag_values_ = values
                return expanded_format_string.format(*tag_values_)
        if num_values > 1:
            return cls.format_multiple_values(
                values[: num_values - 1],
                multiple_values_format,
            )
        return ""

    def format(self, tag_values):
        format_string, conditionals = self.parsed_entry_format
        return dict_re.restore_non_tag_curly_braces(
            format_string.format(
                *[
                    self.format_conditional(conditional, tag_values)
                    for conditional in conditionals
                ]
            )
        )

    def format_conditional(
        self,
        conditional,
        tag_values,
    ):
        for expression in conditional:
            formatted_string = self.format_expression(expression, tag_values)
            if formatted_string:
                return formatted_string
        return ""

    def format_expression(
        self,
        expression,
        tag_values,
    ):
        format_string, tag_list = expression
        try:
            format_string_args = []
            for tag in tag_list:
                formatted_tag_values = self.format_tag_values(
                    tag,
                    tag_values[tag],
                )
                if formatted_tag_values:
                    format_string_args.append(formatted_tag_values)
                else:
                    return ""
            return format_string.format(*format_string_args)
        except KeyError:
            return ""

    def format_tag_values(
        self,
        tag_name,
        tag_values,
    ):
        for (
            format_string,
            order_reversed,
        ) in self.tag_name_to_parsed_tag_values_format[tag_name]:
            num_values = len(tag_values)
            expanded_format_string = (
                dict_re.expand_tag_values_format_expression(
                    format_string,
                    num_values,
                )
            )
            if expanded_format_string:
                if order_reversed:
                    tag_values_ = reversed(tag_values)
                else:
                    tag_values_ = tag_values
                return expanded_format_string.format(*tag_values_)
        return ""


def format_template(template_forms, stem_form):
    forms = []
    for template_form in template_forms:
        form = []
        for template_row, stem_row in zip(
            template_form,
            stem_form,
            strict=True,
        ):
            tag_id, tag_name, template_values = template_row
            tag_id, tag_name, stem_values = stem_row
            values = []
            for i in range(max(len(template_values), len(stem_values))):
                try:
                    template_value = template_values[i]
                except IndexError:
                    template_value = template_values[0]
                try:
                    stem_value = stem_values[i]
                except IndexError:
                    stem_value = ""
                template_value = dict_re.replace_non_tag_curly_braces(
                    template_value
                )
                try:
                    value = template_value.format(stem_value)
                except IndexError:
                    value = template_value
                value = dict_re.restore_non_tag_curly_braces(value)
                values.append(value)
            form.append((tag_id, tag_name, values))
        forms.append(form)
    return forms
