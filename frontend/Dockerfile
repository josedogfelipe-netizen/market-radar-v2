FROM node:18-alpine

WORKDIR /app

# Install dependencies based on package.json
COPY package.json package-lock.json* ./
RUN npm install

# Copy source
COPY . .

# Build not needed for dev, but good for check. 
# For dev we run "npm run dev"
CMD ["npm", "run", "dev"]
