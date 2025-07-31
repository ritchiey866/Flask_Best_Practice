"""
Template filters for Jinja2 templates.
"""
from app.utils.helpers import format_date, truncate_text

def register_template_filters(app):
    """
    Register custom template filters with the Flask app.
    
    Args:
        app: Flask application instance
    """
    
    @app.template_filter('format_date')
    def format_date_filter(date, format_string='%B %d, %Y'):
        """Format date in templates."""
        return format_date(date, format_string)
    
    @app.template_filter('truncate')
    def truncate_filter(text, length=100, suffix='...'):
        """Truncate text in templates."""
        return truncate_text(text, length, suffix)
    
    @app.template_filter('pluralize')
    def pluralize_filter(number, singular, plural=None):
        """Pluralize words based on number."""
        if plural is None:
            plural = singular + 's'
        
        if number == 1:
            return f"{number} {singular}"
        else:
            return f"{number} {plural}"
    
    @app.template_filter('time_ago')
    def time_ago_filter(date):
        """Show relative time (e.g., '2 hours ago')."""
        if not date:
            return ''
        
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        
        if isinstance(date, str):
            try:
                date = datetime.fromisoformat(date.replace('Z', '+00:00'))
            except ValueError:
                return format_date(date)
        
        diff = now - date
        
        if diff.days > 0:
            if diff.days == 1:
                return '1 day ago'
            elif diff.days < 7:
                return f'{diff.days} days ago'
            elif diff.days < 30:
                weeks = diff.days // 7
                if weeks == 1:
                    return '1 week ago'
                else:
                    return f'{weeks} weeks ago'
            elif diff.days < 365:
                months = diff.days // 30
                if months == 1:
                    return '1 month ago'
                else:
                    return f'{months} months ago'
            else:
                years = diff.days // 365
                if years == 1:
                    return '1 year ago'
                else:
                    return f'{years} years ago'
        elif diff.seconds >= 3600:
            hours = diff.seconds // 3600
            if hours == 1:
                return '1 hour ago'
            else:
                return f'{hours} hours ago'
        elif diff.seconds >= 60:
            minutes = diff.seconds // 60
            if minutes == 1:
                return '1 minute ago'
            else:
                return f'{minutes} minutes ago'
        else:
            return 'Just now'
    
    @app.template_filter('word_count')
    def word_count_filter(text):
        """Count words in text."""
        if not text:
            return 0
        return len(text.split())
    
    @app.template_filter('reading_time')
    def reading_time_filter(text, words_per_minute=200):
        """Estimate reading time in minutes."""
        if not text:
            return 0
        
        word_count = len(text.split())
        minutes = max(1, round(word_count / words_per_minute))
        return minutes 