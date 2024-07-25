import ExecutionEnvironment from '@docusaurus/ExecutionEnvironment';

if (ExecutionEnvironment.canUseDOM) {
(function() {
  // List of specific URLs to handle
  const urlsToHandle = [
    '/bolt-python/concepts#adapters',
    '/bolt-python/concepts#async',
    '/bolt-python/concepts#authorization',
    '/bolt-python/concepts#context',
    '/bolt-python/concepts#custom_adapters',
    '/bolt-python/concepts#errors',
    '/bolt-python/concepts#global_middleware',
    '/bolt-python/concepts#lazy_listener',
    '/bolt-python/concepts#listener_middleware',
    '/bolt-python/concepts#logging',
    '/bolt-python/concepts#token_rotation',
    '/bolt-python/concepts#acknowledging_requests',
    '/bolt-python/concepts#authenticating_oauth',
    '/bolt-python/concepts#listening_actions',
    '/bolt-python/concepts#listening_events',
    '/bolt-python/concepts#listening_messages',
    '/bolt-python/concepts#listening_modals',
    '/bolt-python/concepts#listening_responding_commands',
    '/bolt-python/concepts#listening_responding_options',
    '/bolt-python/concepts#listening_responding_shortcuts',
    '/bolt-python/concepts#opening_modals',
    '/bolt-python/concepts#publishing_views',
    '/bolt-python/concepts#responding_actions',
    '/bolt-python/concepts#sending_messages',
    '/bolt-python/concepts#socket_mode',
    '/bolt-python/concepts#updating_pushing_modals',
    '/bolt-python/concepts#web_api',
    '/bolt-python/concepts#adding_editing_workflow_step',
    '/bolt-python/concepts#creating_workflow_step',
    '/bolt-python/concepts#executing_workflow_steps',
    '/bolt-python/concepts#saving_workflow_step',
    '/bolt-python/concepts#workflow_steps_overview',
    '/bolt-python/ja-jp/concepts#adapters',
    '/bolt-python/ja-jp/concepts#async',
    '/bolt-python/ja-jp/concepts#authorization',
    '/bolt-python/ja-jp/concepts#context',
    '/bolt-python/ja-jp/concepts#custom_adapters',
    '/bolt-python/ja-jp/concepts#errors',
    '/bolt-python/ja-jp/concepts#global_middleware',
    '/bolt-python/ja-jp/concepts#lazy_listener',
    '/bolt-python/ja-jp/concepts#listener_middleware',
    '/bolt-python/ja-jp/concepts#logging',
    '/bolt-python/ja-jp/concepts#token_rotation',
    '/bolt-python/ja-jp/concepts#acknowledging_requests',
    '/bolt-python/ja-jp/concepts#authenticating_oauth',
    '/bolt-python/ja-jp/concepts#listening_actions',
    '/bolt-python/ja-jp/concepts#listening_events',
    '/bolt-python/ja-jp/concepts#listening_messages',
    '/bolt-python/ja-jp/concepts#listening_modals',
    '/bolt-python/ja-jp/concepts#listening_responding_commands',
    '/bolt-python/ja-jp/concepts#listening_responding_options',
    '/bolt-python/ja-jp/concepts#listening_responding_shortcuts',
    '/bolt-python/ja-jp/concepts#opening_modals',
    '/bolt-python/ja-jp/concepts#publishing_views',
    '/bolt-python/ja-jp/concepts#responding_actions',
    '/bolt-python/ja-jp/concepts#sending_messages',
    '/bolt-python/ja-jp/concepts#socket_mode',
    '/bolt-python/ja-jp/concepts#updating_pushing_modals',
    '/bolt-python/ja-jp/concepts#web_api',
    '/bolt-python/ja-jp/concepts#adding_editing_workflow_step',
    '/bolt-python/ja-jp/concepts#creating_workflow_step',
    '/bolt-python/ja-jp/concepts#executing_workflow_steps',
    '/bolt-python/ja-jp/concepts#saving_workflow_step',
    '/bolt-python/ja-jp/concepts#workflow_steps_overview'
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
