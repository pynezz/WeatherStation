# syntax=docker/dockerfile:1

FROM node:lts AS base
WORKDIR /app

# Copy the web directory and install dependencies
COPY web ./
RUN npm install

# Build the Astro project
RUN npm run build

ENV HOST=0.0.0.0
ENV PORT=4321
EXPOSE 4321
CMD ["node", "./dist/server/entry.mjs"]

# FROM node:lts AS base
# WORKDIR /app

# # Install PNPM
# RUN npm install -g pnpm

# FROM base AS prod-deps
# WORKDIR /app
# COPY web/package.json web/pnpm-lock.yaml ./
# RUN pnpm install --production

# FROM base AS build-deps
# WORKDIR /app
# COPY web/package.json web/pnpm-lock.yaml ./
# RUN pnpm install --production=false

# FROM build-deps AS build
# # Create a separate directory for the build process to avoid conflicts
# WORKDIR /build
# COPY web ./
# RUN pnpm run build

# FROM base AS runtime
# WORKDIR /app
# COPY --from=prod-deps /app/node_modules ./node_modules
# # Copy the built dist from the /build directory
# COPY --from=build /build/dist ./dist

# ENV HOST=0.0.0.0
# ENV PORT=4321
# EXPOSE 4321
# CMD ["node", "./dist/server/entry.mjs"]


# FROM node:lts AS base
# WORKDIR /app

# # By copying only the package.json and package-lock.json here, we ensure that the following `-deps` steps are independent of the source code.
# # Therefore, the `-deps` steps will be skipped if only the source code changes.
# COPY package.json package-lock.json ./

# FROM base AS prod-deps
# RUN npm install --production

# FROM base AS build-deps
# RUN npm install --production=false

# FROM build-deps AS build
# COPY . .
# RUN npm run build

# FROM base AS runtime
# COPY --from=prod-deps /app/node_modules ./node_modules
# COPY --from=build /app/dist ./dist

# ENV HOST=0.0.0.0
# ENV PORT=4321
# EXPOSE 4321
# CMD node ./dist/server/entry.mjs
