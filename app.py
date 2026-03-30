from project import create_app
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

    
app = create_app()
if __name__ == '__main__':
    app.run(debug=True)

# 必须加这个入口（阿里云要求）
def handler(environ, start_response):
    return app(environ, start_response)
