/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  devIndicators: false, // keep the dev badge out of captured frames
  async redirects() {
    return [{ source: "/", destination: "/en", permanent: false }];
  },
};
export default nextConfig;
