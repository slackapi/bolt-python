import ExecutionEnvironment from '@docusaurus/ExecutionEnvironment';

if (ExecutionEnvironment.canUseDOM) {
(function() {
  // List of specific URLs to handle
  const urlsToHandle = [
        '/bolt-python/concepts#basic',
        '/bolt-python/concepts#advanced',
        '/bolt-python/concepts#message-listening',
        '/bolt-python/concepts#message-sending',
        '/bolt-python/concepts#event-listening',
        '/bolt-python/concepts#web-api',
        '/bolt-python/concepts#action-listening',
        '/bolt-python/concepts#action-respond',
        '/bolt-python/concepts#acknowledge',
        '/bolt-python/concepts#shortcuts',
        '/bolt-python/concepts#commands',
        '/bolt-python/concepts#opening-modals',
        '/bolt-python/concepts#updating-pushing-views',
        '/bolt-python/concepts#view_submissions',
        '/bolt-python/concepts#app-home',
        '/bolt-python/concepts#options',
        '/bolt-python/concepts#authenticating-oauth',
        '/bolt-python/concepts#socket-mode',
        '/bolt-python/concepts#adapters',
        '/bolt-python/concepts#custom-adapters',
        '/bolt-python/concepts#async',
        '/bolt-python/concepts#errors',
        '/bolt-python/concepts#logging',
        '/bolt-python/concepts#authorization',
        '/bolt-python/concepts#token-rotation',
        '/bolt-python/concepts#listener-middleware',
        '/bolt-python/concepts#global-middleware',
        '/bolt-python/concepts#context',
        '/bolt-python/concepts#lazy-listeners',
        '/bolt-python/ja-jp/concepts#message-listening',
        '/bolt-python/ja-jp/concepts#message-sending',
        '/bolt-python/ja-jp/concepts#event-listening',
        '/bolt-python/ja-jp/concepts#web-api',
        '/bolt-python/ja-jp/concepts#action-listening',
        '/bolt-python/ja-jp/concepts#action-respond',
        '/bolt-python/ja-jp/concepts#acknowledge',
        '/bolt-python/ja-jp/concepts#shortcuts',
        '/bolt-python/ja-jp/concepts#commands',
        '/bolt-python/ja-jp/concepts#opening-modals',
        '/bolt-python/ja-jp/concepts#updating-pushing-views',
        '/bolt-python/ja-jp/concepts#view_submissions',
        '/bolt-python/ja-jp/concepts#app-home',
        '/bolt-python/ja-jp/concepts#options',
        '/bolt-python/ja-jp/concepts#authenticating-oauth',
        '/bolt-python/ja-jp/concepts#socket-mode',
        '/bolt-python/ja-jp/concepts#adapters',
        '/bolt-python/ja-jp/concepts#custom-adapters',
        '/bolt-python/ja-jp/concepts#async',
        '/bolt-python/ja-jp/concepts#errors',
        '/bolt-python/ja-jp/concepts#logging',
        '/bolt-python/ja-jp/concepts#authorization',
        '/bolt-python/ja-jp/concepts#token-rotation',
        '/bolt-python/ja-jp/concepts#listener-middleware',
        '/bolt-python/ja-jp/concepts#global-middleware',
        '/bolt-python/ja-jp/concepts#context',
        '/bolt-python/ja-jp/concepts#lazy-listeners',
  ];

  // Get the current path and hash
  const currentPath = window.location.pathname;
  const currentHash = window.location.hash;

  // If there is a hash fragment
  if (currentHash && currentHash.includes('#')) {
    // Create the full URL with hash replaced by '/'
    const newPath = currentPath + currentHash.replace('#', '/');

    // Loop through the list of URLs to handle
    for (const url of urlsToHandle) {
      // Check if the current path matches the URL to handle
      if (currentPath === url.split('#')[0] && window.location.hash === `#${url.split('#')[1]}`) {
        // Redirect to the new path
        window.location.replace(newPath);
        return; // Exit after the first match
      }
    }
  }
})();
}
