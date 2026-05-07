import { resolve } from "path";
import { defineConfig } from "vite";

const mainEntry = resolve(__dirname, "django_music/assets/entry.js");
const staticOutDir = resolve(__dirname, "django_music/static");

export default defineConfig({
    publicDir: false,
    build: {
        emptyOutDir: false,
        outDir: staticOutDir,
        cssCodeSplit: false,
        rollupOptions: {
            input: mainEntry,
            output: {
                entryFileNames: "dist/[name].js",
                chunkFileNames: "dist/[name].js",
                assetFileNames: ({ name }) => {
                    if (name && name.endsWith(".css")) {
                        return "dist/[name].css";
                    }

                    return "assets/[name].[ext]";
                },
            },
        },
    },
});
