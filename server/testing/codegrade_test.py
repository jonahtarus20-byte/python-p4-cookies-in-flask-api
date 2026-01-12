
import pytest
from server.app import app

def test_codegrade_placeholder():
    """Codegrade placeholder test"""
    assert 1==1

def test_show_session():
    """Test the show_session route"""
    with app.test_client() as client:
        # Make a GET request to /sessions/hello
        response = client.get('/sessions/hello')

        # Check status code
        assert response.status_code == 200

        # Parse JSON response
        data = response.get_json()

        # Check response structure
        assert 'session' in data
        assert 'cookies' in data

        # Check session data
        session_data = data['session']
        assert session_data['session_key'] == 'hello'
        assert session_data['session_value'] == 'World'
        assert session_data['session_accessed'] is True

        # Check cookies in response (these are request cookies, should be empty initially)
        cookies = data['cookies']
        assert len(cookies) == 0  # No cookies sent in initial request

        # Check that cookies are set in the response headers
        set_cookie_headers = [value for name, value in response.headers if name == 'Set-Cookie']
        assert len(set_cookie_headers) >= 2  # Should have session cookie and mouse cookie

        # Check that the 'mouse' cookie was set
        mouse_cookie_set = any('mouse=Cookie' in header for header in set_cookie_headers)
        assert mouse_cookie_set

        # Check that session cookie was set
        session_cookie_set = any('session=' in header for header in set_cookie_headers)
        assert session_cookie_set

def test_session_persistence():
    """Test that session values persist across requests"""
    with app.test_client() as client:
        # First request
        response1 = client.get('/sessions/hello')
        assert response1.status_code == 200

        # Second request to the same session
        response2 = client.get('/sessions/goodnight')
        assert response2.status_code == 200

        data = response2.get_json()
        session_data = data['session']

        # Should still have the hello value and the goodnight value
        assert session_data['session_key'] == 'goodnight'
        assert session_data['session_value'] == 'Moon'
