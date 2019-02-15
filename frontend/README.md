```bash
.
├── .gitignore                # Tells git which files to ignore
├── dist                      # Folder where the build script places the built app. Use this in prod.
├── package.json              # Package configuration. The list of 3rd party libraries and utilities
├── src                       # Source code
│   ├── components            # React components
│   ├── config                # Configuration files, like constants
│   ├── routes                # Application routes and route components
│   ├── favicon.ico           # favicon to keep your browser from throwing a 404 during dev. Not actually used in prod build.
│   ├── index.ejs             # Template for homepage
│   ├── index.ts              # Entry point for your app
│   ├── store                 # Redux store configuration
       ├── reducers.ts        # Redux reducers. Your state is altered here based on actions  
       ├── actions .ts        # Redux actions. List of distinct actions that can occur in the app.
│   ├── styles                # CSS Styles, typically written in Sass
│   └── utils                 # JS helpers
├── tools                     # Node scripts that run build related tools
│   └── analyzeBundle.js      # Analyzes the webpack bundle
│   ├── assetsTransformer.js  # Fix for jest handling static assets like imported images
│   ├── build.js              # Runs the production build
│   ├── chalkConfig.js        # Centralized configuration for chalk (adds color to console statements)
│   ├── distServer.js         # Starts webserver and opens final built app that's in dist in your default browser
│   ├── nodeVersionCheck.js   # Confirm supported Node version is installed
│   ├── srcServer.js          # Starts dev webserver with hot reloading and opens your app in your default browser
│   ├── startMessage.js       # Display message when development build starts
├── Webpack  		
│   ├── webpack.config.dev.js     # Configures webpack for development builds
│   └── webpack.config.prod.js    # Configures webpack for production builds
```
