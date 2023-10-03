from unittest import TestCase
from templatex.engine import escape_latex, get_jinja_env_args, get_jinja_filters, Environment, Template
from unittest.mock import patch, MagicMock


class TestTemplatex(TestCase):
    def test_ampersand_escape(self):
        self.assertEqual(escape_latex('&'), r'\&')

    def test_percentage_escape(self):
        self.assertEqual(escape_latex('%'), r'\%')

    def test_dollar_escape(self):
        self.assertEqual(escape_latex('$'), r'\$')

    def test_hash_escape(self):
        self.assertEqual(escape_latex('#'), r'\#')

    def test_underscore_escape(self):
        self.assertEqual(escape_latex('_'), r'\_')

    def test_curly_braces_escape(self):
        self.assertEqual(escape_latex('{'), r'\{')
        self.assertEqual(escape_latex('}'), r'\}')

    def test_tilde_escape(self):
        self.assertEqual(escape_latex('~'), r'\textasciitilde{}')

    def test_caret_escape(self):
        self.assertEqual(escape_latex('^'), r'\^{}')

    def test_backslash_escape(self):
        self.assertEqual(escape_latex('\\'), r'\textbackslash{}')

    def test_angle_brackets_escape(self):
        self.assertEqual(escape_latex('<'), r'\textless{}')
        self.assertEqual(escape_latex('>'), r'\textgreater{}')

    def test_mixed_content(self):
        original = "This & that $100 #tag _underscore {set} ~tilde ^caret \\backslash <less >greater"
        expected = (r"This \& that \$100 \#tag \_underscore \{set\} \textasciitilde{}tilde \^{}caret "
                    r"\textbackslash{}backslash \textless{}less \textgreater{}greater")
        self.assertEqual(escape_latex(original), expected)

    def test_get_jinja_env_args(self):
        env_args = get_jinja_env_args()
        env_args2 = get_jinja_env_args()

        self.assertEqual(env_args, env_args2)

        env_args['autoescape'] = True

        self.assertNotEqual(env_args, env_args2)

    def test_get_jinja_filters(self):
        filters = get_jinja_filters()
        filters2 = get_jinja_filters()

        self.assertEqual(filters, filters2)
        filters2['s'] = lambda x: str(x)

        self.assertNotEqual(filters, filters2)

    @patch('templatex.engine.Jinja2Environment')  # Replace 'your_module_name' with the actual module name
    def test_env_initialization(self, MockEnvironment):
        mock_loader = MagicMock()
        env_instance = MagicMock()
        env_instance.filters = {}

        MockEnvironment.return_value = env_instance

        env = Environment(mock_loader)

        env_args = get_jinja_env_args()
        filters = get_jinja_filters()

        MockEnvironment.assert_called_once_with(loader=mock_loader, **env_args)
        self.assertEqual(env_instance.filters, filters)

    @patch('templatex.engine.Jinja2Environment')
    def test_env_with_override(self, MockEnvironment):
        mock_loader = MagicMock()
        env_instance = MagicMock()
        env_instance.filters = {}

        MockEnvironment.return_value = env_instance
        override = {'autoescape': True}

        env = Environment(mock_loader, **override)

        env_args = get_jinja_env_args()
        filters = get_jinja_filters()

        expected_filters = {**env_args, **override}
        MockEnvironment.assert_called_once_with(loader=mock_loader, **expected_filters)
        self.assertEqual(env_instance.filters, filters)

    @patch('templatex.engine.Jinja2Template')
    def test_template_creation(self, MockTemplate):
        template_instance = MagicMock()

        MockTemplate.return_value = template_instance
        override = {'autoescape': True}

        env = Template('abc', autoescape=True)

        expected_env_args = get_jinja_env_args()
        expected_env_args['autoescape'] = True

        MockTemplate.assert_called_once_with('abc', **expected_env_args)
