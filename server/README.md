# Bob Server

### Installation

```bash
npm install
```

### Starting the server
```
npm start
```

### Development
Instead of `npm start`, use:
```bash
npm run dev
```
This will restart the server whenever you change a file.

*Note: Please install the [Prettier Plugin](https://prettier.io/docs/en/editors.html) on your preferred text editor.*

### Running tests
```bash
npm test
```

### Configuration
Change these environment variables before running the server:
```
PORT=9000                            # Port the server will run on.
MONGO=mongodb://localhost:27017/db   # URL of the mongo instance
```