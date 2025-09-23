# Tech Hive

Tech Hive is a thriving tech hub for tech enthusiasts and professionals.

## Overview

A modern, collaborative platform for the tech community featuring article writing, job listings, resource sharing, and tool discovery. Built with React, TypeScript, and real-time collaboration powered by Liveblocks.

## ✅ Features Completed

### Core Features
- ✅ **Featured Tech Tools** - Discover and explore trending tech tools
- ✅ **Tech Jobs** - Browse and post tech job opportunities  
- ✅ **Tech Articles** - Rich text editor with collaborative writing
- ✅ **Resource Spotlight** - Curated tech resources and learning materials

### Article Editor
- ✅ **Rich Text Editor** - Full-featured TipTap editor
- ✅ **Real-time Collaboration** - Multi-user editing with Liveblocks
- ✅ **Text Formatting** - Bold, italic, underline, code blocks, etc.
- ✅ **Lists & Headings** - Ordered/unordered lists, heading levels
- ✅ **Links & Media** - Link insertion, YouTube video embedding
- ✅ **Tables** - Full table support with editing capabilities
- ✅ **Text Alignment** - Left, center, right alignment
- ✅ **Code Syntax Highlighting** - Prism.js integration with lowlight
- ✅ **Image Upload** - Basic image insertion functionality
- ✅ **Help System** - Built-in help and documentation

### UI/UX
- ✅ **Modern Design** - Clean, responsive interface
- ✅ **Theme Support** - Light/dark mode implementation
- ✅ **Toast Notifications** - User feedback system
- ✅ **Custom Toolbar** - Comprehensive editing toolbar

## 🚧 Roadmap

### Phase 1: Core Improvements (Priority: High)
- [ ] **Backend API Integration**
  - [ ] Connect frontend to backend services
  - [ ] Implement authentication flow
  - [ ] Add data persistence for articles, jobs, resources
  - [ ] User management and profiles

- [ ] **Image Management Overhaul**
  - [ ] Replace blob URLs with localStorage for temporary storage
  - [ ] Implement IndexedDB fallback for large images
  - [ ] Only save images to backend on article save/publish
  - [ ] Alt text support for accessibility

- [ ] **Code Quality & Maintenance**
  - [ ] Audit and resolve all TODO comments
  - [ ] Fix all FIXME items in codebase
  - [ ] Code refactoring for better maintainability
  - [ ] Remove unused dependencies and dead code

- [ ] **Documentation & DevOps**
  - ✅ Create comprehensive docs page for editor help section
  - [ ] Dockerize the application for consistent deployment
  

### Phase 2: Performance & UX (Priority: High)
- [ ] **Loading States & Skeleton UI**
  - [ ] Article list skeleton loaders
  - [ ] Job listings skeleton loaders  
  - [ ] Resource cards skeleton loaders
  - ✅ Editor loading states
  - ✅ Image upload progress indicators

- [ ] **Performance Optimization**
  - [ ] Implement lazy loading for images
  - [ ] Code splitting and bundle optimization
  - [ ] Memoization for expensive computations
  - [ ] Virtual scrolling for large lists
  - [ ] Performance testing and monitoring

- [ ] **Accessibility (A11y)**
  - [ ] ARIA labels and roles
  - [ ] Keyboard navigation support
  - [ ] Screen reader compatibility
  - [ ] Color contrast compliance
  - [ ] Focus management
  - [ ] Alt text for all images

### Phase 3: Advanced Features (Priority: Medium)
- [ ] **Enhanced Editor Features**
  - [ ] Custom blocks (callouts, quotes, etc.)

- [ ] **Search & Discovery**
  - [ ] Full-text search across articles
  - [ ] Advanced filtering options
  - [ ] Recommendation engine

### Phase 4: Advanced Functionality (Priority: Low)
- [ ] **Analytics & Insights**
  - [ ] Reading analytics for authors
  - [ ] Popular content tracking
  - [ ] User engagement metrics
  - [ ] SEO optimization tools

- [ ] **Mobile Experience**
  - [ ] Progressive Web App (PWA)
  - [ ] Mobile-optimized editor
  - [ ] Offline reading capability
  - [ ] Push notifications

- [ ] **Content Management**
  - [ ] Editorial workflow
  - [ ] Content moderation tools

## 🛠 Technical Stack

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **TailwindCSS** - Styling framework
- **TipTap** - Rich text editor
- **Liveblocks** - Real-time collaboration
- **React Hot Toast** - Notifications

### Editor Extensions
- **Lowlight + Highlight JS** - Code syntax highlighting
- **TailwindCSS Typography** - Content styling

## 📚 Useful Resources

- [TipTap Headings & Lists Issue](https://stackoverflow.com/questions/78057571/why-isnt-the-headings-and-lists-working-in-tiptap)
- [TailwindCSS Typography Plugin](https://github.com/tailwindlabs/tailwindcss-typography)
- [TipTap Update Attributes API](https://tiptap.dev/docs/editor/api/commands/nodes-and-marks/update-attributes)
- [TipTap Image Upload Guide](https://stackoverflow.com/questions/78147060/how-to-upload-inserted-images-with-image-extension-in-tiptap)
- [TipTap Node Selection Issue](https://stackoverflow.com/questions/78161917/updating-attributes-on-the-image-caused-the-node-to-be-deselected-in-tiptap)
- [How to add editing image alt tiptap](https://angelika.me/2023/02/26/how-to-add-editing-image-alt-text-tiptap/)
- [Tiptap Drag Drop Image](https://www.codemzy.com/blog/tiptap-drag-drop-image)
- [Render server error with React hook form](https://react-hook-form.com/get-started)
- [Mutations in React Query](https://tkdodo.eu/blog/mastering-mutations-in-react-query)
- [How integrate refresh token in React Reddit](https://www.reddit.com/r/reactjs/comments/1ejtu9h/how_to_integrate_refresh_tokens_in_react/)
- [How integrate refresh token in React](https://rabbitbyte.club/how-to-integrate-refresh-tokens-in-react-app/)


## 🚀 Getting Started

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

## 🤝 Contributing

1. Check the roadmap above for current priorities
2. Look for TODO and FIXME comments in the codebase
3. Focus on Phase 1 items for maximum impact
4. Ensure accessibility compliance for all new features
5. Add appropriate loading states and error handling
