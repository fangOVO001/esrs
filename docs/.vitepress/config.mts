import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Recommand Shopping Develop Log",
  description: "Develop Blog",
  base: "/esrs",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
    ],

    sidebar: [
      {
        text: 'Develop Log',
        items: [
          { text: '2024-04-14', link: '/2024-04-14' },
          { text: '2024-04-16', link: '/2024-04-16' },
          { text: '2024-04-18', link: '/2024-04-18' },
          { text: '2024-04-20', link: '/2024-04-20' },
          { text: '2024-04-27', link: '/2024-04-27' },
          { text: '2024-05-01', link: '/2024-05-01' },
          { text: '2024-05-05', link: '/2024-05-05' },
          { text: '2024-05-10', link: '/2024-05-10' }
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/vuejs/vitepress' }
    ]
  }
})
