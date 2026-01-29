# Component Pattern Guide

## Button Patterns

### Primary Button
```tsx
<button className="bg-[#primary] hover:bg-[#primary-hover] text-white
                   py-3 px-6 rounded-lg font-medium transition-all duration-200">
  Button Text
</button>
```

### Secondary Button
```tsx
<button className="bg-transparent hover:bg-[#secondary-hover]
                   text-[#secondary] hover:text-white
                   border border-[#secondary] hover:border-transparent
                   py-3 px-6 rounded-lg font-medium transition-all duration-200">
  Button Text
</button>
```

### Ghost Button
```tsx
<button className="bg-transparent hover:bg-white/10
                   text-[#text] hover:text-white
                   py-2 px-4 rounded-md font-medium transition-all duration-200">
  Button Text
</button>
```

### Chip/Tag Button
```tsx
<button className="inline-flex items-center gap-2
                   bg-[#chip-bg] hover:bg-[#chip-hover]
                   text-[#chip-text] hover:text-white
                   py-3 px-4 rounded-3xl text-sm font-medium
                   transition-all duration-200">
  <Icon className="w-4 h-4" />
  <span>Label</span>
</button>
```

### Icon Button
```tsx
<button className="p-2 rounded-full
                   bg-transparent hover:bg-white/10
                   text-[#icon] hover:text-white
                   transition-all duration-200">
  <Icon className="w-5 h-5" />
</button>
```

## Input Field Patterns

### Basic Text Input
```tsx
<input
  type="text"
  className="w-full px-4 py-3
             bg-[#input-bg] text-[#input-text]
             border border-[#input-border] focus:border-[#input-focus]
             rounded-lg outline-none
             placeholder:text-[#placeholder]
             transition-colors duration-200"
  placeholder="Enter text..."
/>
```

### Input with Gradient Border
```tsx
<div className="p-[1px] rounded-3xl bg-gradient-to-r from-[#gradient-start] to-[#gradient-end]">
  <div className="bg-[#input-bg] rounded-[calc(1.5rem-1px)]">
    <input
      className="w-full p-4 bg-transparent text-white
                 outline-none placeholder:text-[#placeholder]"
      placeholder="Enter text..."
    />
  </div>
</div>
```

### Search Input with Icon
```tsx
<div className="relative">
  <SearchIcon className="absolute left-4 top-1/2 -translate-y-1/2
                         w-5 h-5 text-[#icon]" />
  <input
    type="search"
    className="w-full pl-12 pr-4 py-3
               bg-[#input-bg] text-[#input-text]
               border border-[#input-border] focus:border-[#input-focus]
               rounded-full outline-none
               placeholder:text-[#placeholder]
               transition-colors duration-200"
    placeholder="Search..."
  />
</div>
```

## Card Patterns

### Basic Card
```tsx
<div className="bg-[#card-bg] rounded-2xl p-6 shadow-lg">
  <h3 className="text-lg font-semibold text-[#card-title] mb-2">
    Card Title
  </h3>
  <p className="text-[#card-text]">
    Card content goes here.
  </p>
</div>
```

### Card with Image
```tsx
<div className="bg-[#card-bg] rounded-2xl overflow-hidden shadow-lg">
  <img
    src="image.jpg"
    alt="Card image"
    className="w-full h-48 object-cover"
  />
  <div className="p-6">
    <h3 className="text-lg font-semibold text-[#card-title] mb-2">
      Card Title
    </h3>
    <p className="text-[#card-text]">
      Card content goes here.
    </p>
  </div>
</div>
```

### Interactive Card
```tsx
<div className="bg-[#card-bg] hover:bg-[#card-hover]
                rounded-2xl p-6 shadow-lg
                cursor-pointer transition-all duration-200
                hover:shadow-xl hover:-translate-y-1">
  <h3 className="text-lg font-semibold text-[#card-title] mb-2">
    Card Title
  </h3>
  <p className="text-[#card-text]">
    Card content goes here.
  </p>
</div>
```

### Glass Card (Glassmorphism)
```tsx
<div className="bg-white/10 backdrop-blur-lg
                border border-white/20
                rounded-2xl p-6 shadow-lg">
  <h3 className="text-lg font-semibold text-white mb-2">
    Glass Card
  </h3>
  <p className="text-white/80">
    Content with glassmorphism effect.
  </p>
</div>
```

## Container Patterns

### Page Container
```tsx
<div className="min-h-screen bg-[#page-bg]">
  <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    {/* Page content */}
  </div>
</div>
```

### Modal/Dialog Container
```tsx
<div className="fixed inset-0 z-50 flex items-center justify-center">
  {/* Backdrop */}
  <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" />

  {/* Modal */}
  <div className="relative bg-[#modal-bg] rounded-2xl p-8
                  max-w-lg w-full mx-4 shadow-2xl">
    <h2 className="text-xl font-semibold text-[#modal-title] mb-4">
      Modal Title
    </h2>
    <p className="text-[#modal-text] mb-6">
      Modal content goes here.
    </p>
    <div className="flex justify-end gap-3">
      <button className="px-4 py-2 rounded-lg text-[#btn-secondary]">
        Cancel
      </button>
      <button className="px-4 py-2 rounded-lg bg-[#primary] text-white">
        Confirm
      </button>
    </div>
  </div>
</div>
```

## Navigation Patterns

### Navbar
```tsx
<nav className="fixed top-0 left-0 right-0 z-40
                bg-[#nav-bg]/80 backdrop-blur-lg
                border-b border-[#nav-border]">
  <div className="max-w-7xl mx-auto px-4 h-16
                  flex items-center justify-between">
    <Logo />
    <div className="flex items-center gap-6">
      <NavLink href="/">Home</NavLink>
      <NavLink href="/about">About</NavLink>
    </div>
  </div>
</nav>
```

### Sidebar
```tsx
<aside className="fixed left-0 top-0 bottom-0 w-64
                  bg-[#sidebar-bg] border-r border-[#sidebar-border]
                  flex flex-col">
  <div className="p-4 border-b border-[#sidebar-border]">
    <Logo />
  </div>
  <nav className="flex-1 p-4 space-y-2">
    <SidebarLink icon={HomeIcon} href="/">Home</SidebarLink>
    <SidebarLink icon={SettingsIcon} href="/settings">Settings</SidebarLink>
  </nav>
</aside>
```

## Badge/Tag Patterns

### Status Badge
```tsx
<span className="inline-flex items-center px-2.5 py-0.5
                 rounded-full text-xs font-medium
                 bg-[#badge-bg] text-[#badge-text]">
  Active
</span>
```

### Removable Tag
```tsx
<span className="inline-flex items-center gap-1 px-3 py-1
                 rounded-full text-sm
                 bg-[#tag-bg] text-[#tag-text]">
  Tag Label
  <button className="hover:text-[#tag-remove-hover]">
    <XIcon className="w-3 h-3" />
  </button>
</span>
```

## Animation Patterns

### Fade In
```tsx
<div className="animate-fadeIn">
  {/* Content fades in */}
</div>

// tailwind.config.js:
// animation: { fadeIn: 'fadeIn 0.3s ease-out' }
// keyframes: { fadeIn: { '0%': { opacity: '0' }, '100%': { opacity: '1' } } }
```

### Slide Up
```tsx
<div className="animate-slideUp">
  {/* Content slides up */}
</div>

// tailwind.config.js:
// animation: { slideUp: 'slideUp 0.3s ease-out' }
// keyframes: { slideUp: { '0%': { transform: 'translateY(10px)', opacity: '0' }, '100%': { transform: 'translateY(0)', opacity: '1' } } }
```
