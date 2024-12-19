/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
	sidebarBoltPy: [
		{
			type: "doc",
			id: "index",
			label: "Bolt for Python",
			className: "sidebar-title",
		},
		{ type: "html", value: "<hr>" },
		{
			type: "category",
			label: "Guides",
			collapsed: false,
			items: [
				"getting-started",
				{
					type: "category",
					label: "Basic concepts",
					items: [
						"basic/assistant",
						"basic/message-listening",
						"basic/message-sending",
						"basic/event-listening",
						"basic/web-api",
						"basic/action-listening",
						"basic/action-respond",
						"basic/acknowledge",
						"basic/shortcuts",
						"basic/commands",
						"basic/opening-modals",
						"basic/updating-pushing-views",
						"basic/view_submissions",
						"basic/app-home",
						"basic/options",
						"basic/custom-steps",
						"basic/authenticating-oauth",
						"basic/socket-mode",
					],
				},
				{
					type: "category",
					label: "Advanced concepts",
					items: [
						"advanced/adapters",
						"advanced/custom-adapters",
						"advanced/async",
						"advanced/errors",
						"advanced/logging",
						"advanced/authorization",
						"advanced/token-rotation",
						"advanced/listener-middleware",
						"advanced/global-middleware",
						"advanced/context",
						"advanced/lazy-listeners",
					],
				},
				{
					type: "category",
					label: "Steps from apps (Deprecated)",
					items: [
						"steps/steps",
						"steps/executing-steps",
						"steps/creating-steps",
						"steps/adding-editing-steps",
						"steps/saving-steps",
					],
				},
			],
		},
		{ type: "html", value: "<hr>" },
		{
			type: "category",
			label: "Tutorials",
			items: [
				"tutorial/getting-started-http",
				"tutorial/ai-chatbot",
				"tutorial/custom-steps-for-jira",
			],
		},
		{ type: "html", value: "<hr>" },
		{
			type: "link",
			label: "Reference",
			href: "https://tools.slack.dev/bolt-python/api-docs/slack_bolt/",
		},
		{ type: "html", value: "<hr>" },
		{
			type: "link",
			label: "Release notes",
			href: "https://github.com/slackapi/bolt-python/releases",
		},
		{
			type: "link",
			label: "Code on GitHub",
			href: "https://github.com/SlackAPI/bolt-python",
		},
		{
			type: "link",
			label: "Contributors Guide",
			href: "https://github.com/SlackAPI/bolt-python/blob/main/.github/contributing.md",
		},
	],
};

export default sidebars;
