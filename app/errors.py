"""
Error handlers for the Flask application.
"""
from flask import render_template, request, jsonify
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    """
    Register error handlers with the Flask app.
    
    Args:
        app: Flask application instance
    """
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 Bad Request errors."""
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Bad Request',
                'message': 'The request could not be processed.',
                'status_code': 400
            }), 400
        
        return render_template('errors/400.html'), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        """Handle 401 Unauthorized errors."""
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Authentication required.',
                'status_code': 401
            }), 401
        
        return render_template('errors/401.html'), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        """Handle 403 Forbidden errors."""
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Forbidden',
                'message': 'You do not have permission to access this resource.',
                'status_code': 403
            }), 403
        
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found errors."""
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Not Found',
                'message': 'The requested resource was not found.',
                'status_code': 404
            }), 404
        
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle 405 Method Not Allowed errors."""
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Method Not Allowed',
                'message': 'The method is not allowed for this resource.',
                'status_code': 405
            }), 405
        
        return render_template('errors/405.html'), 405
    
    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle 500 Internal Server Error."""
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Internal Server Error',
                'message': 'An unexpected error occurred.',
                'status_code': 500
            }), 500
        
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        """Handle general HTTP exceptions."""
        if request.path.startswith('/api/'):
            return jsonify({
                'error': error.name,
                'message': error.description,
                'status_code': error.code
            }), error.code
        
        return render_template('errors/generic.html', error=error), error.code
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle unhandled exceptions."""
        # Log the error here in production
        app.logger.error(f'Unhandled exception: {error}')
        
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Internal Server Error',
                'message': 'An unexpected error occurred.',
                'status_code': 500
            }), 500
        
        return render_template('errors/500.html'), 500 