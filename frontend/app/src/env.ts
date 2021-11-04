export const API_URL: string = env("REACT_APP_API");

export function env(name: string): string {
    const value = process.env[name];

    if (!value) {
        throw new Error(`Missing: process.env['${name}'].`);
    }

    return value;
}
