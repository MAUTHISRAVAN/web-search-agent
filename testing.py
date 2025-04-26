import unittest
from unittest.mock import Mock, patch
from src.agent import WebResearchAgent

class TestWebResearchAgent(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        self.agent = WebResearchAgent(api_key="test_key")

    def test_analyze_query(self):
        """Test query analysis functionality"""
        test_query = "What are the latest developments in quantum computing?"
        
        with patch('langchain.llms.OpenAI.generate') as mock_llm:
            mock_llm.return_value = {
                "main_topics": ["quantum computing", "recent developments"],
                "info_type": "recent news and facts",
                "search_terms": ["quantum computing breakthroughs", "recent quantum developments"]
            }
            
            result = self.agent.analyze_query(test_query)
            
            self.assertIsInstance(result, dict)
            self.assertIn('main_topics', result)
            self.assertIn('info_type', result)
            self.assertIn('search_terms', result)

    def test_search_tool(self):
        """Test web search tool functionality"""
        with patch('src.tools.search_tool.WebSearchTool.search') as mock_search:
            mock_search.return_value = {
                "urls": ["http://example.com/1", "http://example.com/2"],
                "snippets": ["Snippet 1", "Snippet 2"],
                "titles": ["Title 1", "Title 2"]
            }
            
            result = self.agent.search_tool.search("test query")
            
            self.assertIsInstance(result, dict)
            self.assertIn('urls', result)
            self.assertIn('snippets', result)
            self.assertEqual(len(result['urls']), 2)

    def test_error_handling(self):
        """Test error handling in research pipeline"""
        with patch('src.tools.search_tool.WebSearchTool.search') as mock_search:
            mock_search.side_effect = Exception("Search API error")
            
            with self.assertRaises(Exception):
                self.agent.conduct_research("test query")

    def test_content_synthesis(self):
        """Test content synthesis functionality"""
        test_content = {
            "raw_content": ["Content 1", "Content 2"],
            "analyzed_data": {"key_points": ["Point 1", "Point 2"]},
            "news": {"articles": ["News 1", "News 2"]}
        }
        
        result = self.agent._synthesize_results(test_content)
        
        self.assertIsInstance(result, dict)
        self.assertIn('summary', result)
        self.assertIn('sources', result)

class TestWebScraperTool(unittest.TestCase):
    def setUp(self):
        self.scraper = WebScraperTool()

    def test_scrape_valid_url(self):
        """Test scraping from a valid URL"""
        with patch('requests.get') as mock_get:
            mock_get.return_value.text = "<html><body><p>Test content</p></body></html>"
            mock_get.return_value.status_code = 200
            
            result = self.scraper.scrape("http://example.com")
            
            self.assertIsInstance(result, str)
            self.assertIn("Test content", result)

    def test_scrape_invalid_url(self):
        """Test scraping from an invalid URL"""
        with patch('requests.get') as mock_get:
            mock_get.side_effect = Exception("404 Not Found")
            
            with self.assertRaises(Exception):
                self.scraper.scrape("http://invalid-url.com")

class TestContentAnalyzerTool(unittest.TestCase):
    def setUp(self):
        self.analyzer = ContentAnalyzerTool()

    def test_analyze_content(self):
        """Test content analysis functionality"""
        test_content = ["Sample content 1", "Sample content 2"]
        
        result = self.analyzer.analyze(test_content)
        
        self.assertIsInstance(result, dict)
        self.assertIn('key_points', result)
        self.assertIn('sentiment', result)

if __name__ == '__main__':
    unittest.main()
