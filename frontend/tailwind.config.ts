import type { Config } from "tailwindcss";

const config: Config = {
    content: [
        "./app/**/*.{js,ts,jsx,tsx,mdx}",
        "./components/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
        extend: {
            colors: {
                background: "var(--background)",
                foreground: "var(--foreground)",
                radar: {
                    red: "#ef4444",
                    yellow: "#eab308",
                    green: "#22c55e",
                    dark: "#0f172a"
                }
            },
        },
    },
    plugins: [],
};
export default config;
