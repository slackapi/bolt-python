/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  sidebarBoltPy: [
    {
      type: 'doc',
      id: 'index',
      label: 'Bolt for Python',
      className: 'sidebar-title',
    },
    'getting-started',
    {
      type: "category",
      label: "Slack API calls",
      items: ["concepts/message-sending", "concepts/web-api"],
    },
    {
      type: "category",
      label: "Events API",
      items: ["concepts/message-listening", "concepts/event-listening"],
    },
    {
      type: "category",
      label: "App UI & Interactivity",
      items: [
        "concepts/acknowledge",
        "concepts/shortcuts",
        "concepts/commands",
        "concepts/actions",
        "concepts/opening-modals",
        "concepts/updating-pushing-views",
        "concepts/view-submissions",
        "concepts/select-menu-options",
        "concepts/app-home",
      ],
    },
    'concepts/assistant',
    'concepts/custom-steps',
    {
      type: "category",
      label: "App Configuration",
      items: [
        "concepts/socket-mode",
        "concepts/errors",
        "concepts/logging",
        'concepts/async',
      ],
    },
    {
      type: "category",
      label: "Middleware & Adaptors",
      items: [
        "concepts/global-middleware",
        "concepts/listener-middleware",
        'concepts/lazy-listeners',
        'concepts/context',
        'concepts/adapters',
        'concepts/custom-adapters',
      ],
    },
    {
      type: "category",
      label: "Authorization & Security",
      items: [
        "concepts/authenticating-oauth",
        "concepts/authorization",
        "concepts/token-rotation",
      ],
    },
    {
      type: 'category',
      label: 'Legacy',
      items: [
        'concepts/steps-from-apps',
      ],
    },
    { type: 'html', value: '<hr>' },
    {
      type: 'category',
      label: 'Tutorials',
      items: [
        'tutorial/ai-chatbot'
      ],
    },
    { type: 'html', value: '<hr>' },
    {
      type: 'link',
      label: 'Reference',
      href: 'https://tools.slack.dev/bolt-python/api-docs/slack_bolt/',
    },
    { type: 'html', value: '<hr>' },
    {
      type: 'link',
      label: 'Release notes',
      href: 'https://github.com/slackapi/bolt-python/releases',
    },
    {
      type: 'link',
      label: 'Code on GitHub',
      href: 'https://github.com/SlackAPI/bolt-python',
    },
    {
      type: 'link',
      label: 'Contributors Guide',
      href: 'https://github.com/SlackAPI/bolt-python/blob/main/.github/contributing.md',
    },
  ],
};

export default sidebars;
