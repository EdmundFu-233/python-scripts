"""Terminal color output utilities"""
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    
    @staticmethod
    def info(msg: str):
        print(f"{Colors.CYAN}[INFO]{Colors.END} {msg}")
    
    @staticmethod
    def success(msg: str):
        print(f"{Colors.GREEN}[OK]{Colors.END} {msg}")
    
    @staticmethod
    def warning(msg: str):
        print(f"{Colors.WARNING}[WARN]{Colors.END} {msg}")
    
    @staticmethod
    def error(msg: str):
        print(f"{Colors.FAIL}[ERROR]{Colors.END} {msg}")
    
    @staticmethod
    def header(msg: str):
        print(f"{Colors.BOLD}{Colors.BLUE}{msg}{Colors.END}")

if __name__ == "__main__":
    Colors.header("System Check")
    Colors.info("Checking status...")
    Colors.success("All systems operational")
