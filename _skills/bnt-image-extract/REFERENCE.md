# Tailwind CSS Mapping Reference

## Color Conversion

### RGB to Tailwind
```
rgb(r, g, b) → #rrggbb → bg-[#rrggbb] or text-[#rrggbb]
```

### Common Color Mapping
| RGB | Hex | Tailwind |
|-----|-----|----------|
| rgb(0,0,0) | #000000 | black |
| rgb(255,255,255) | #ffffff | white |
| rgb(26,115,232) | #1a73e8 | blue-600 (approx) |
| rgb(32,33,36) | #202124 | gray-900 (approx) |
| rgb(189,193,198) | #bdc1c6 | gray-400 (approx) |

### RGBA Handling
```
rgba(r, g, b, a) → bg-[#rrggbb]/[opacity]
Example: rgba(0,0,0,0.5) → bg-black/50
```

## Spacing Conversion

### Tailwind Spacing Scale
| px | Tailwind | rem |
|----|----------|-----|
| 0 | 0 | 0 |
| 1 | px | 1px |
| 2 | 0.5 | 0.125rem |
| 4 | 1 | 0.25rem |
| 6 | 1.5 | 0.375rem |
| 8 | 2 | 0.5rem |
| 10 | 2.5 | 0.625rem |
| 12 | 3 | 0.75rem |
| 14 | 3.5 | 0.875rem |
| 16 | 4 | 1rem |
| 20 | 5 | 1.25rem |
| 24 | 6 | 1.5rem |
| 28 | 7 | 1.75rem |
| 32 | 8 | 2rem |
| 36 | 9 | 2.25rem |
| 40 | 10 | 2.5rem |
| 44 | 11 | 2.75rem |
| 48 | 12 | 3rem |
| 56 | 14 | 3.5rem |
| 64 | 16 | 4rem |
| 80 | 20 | 5rem |
| 96 | 24 | 6rem |

### Conversion Rules
1. Use exact match if available
2. Allow ±2px tolerance
3. Use arbitrary value if no match: `p-[13px]`

### Padding/Margin Prefixes
| Property | Prefix |
|----------|--------|
| padding | p- |
| padding-top | pt- |
| padding-right | pr- |
| padding-bottom | pb- |
| padding-left | pl- |
| padding-x (left+right) | px- |
| padding-y (top+bottom) | py- |
| margin | m- |
| margin-top | mt- |
| margin-right | mr- |
| margin-bottom | mb- |
| margin-left | ml- |
| margin-x | mx- |
| margin-y | my- |

## Border Radius

| px | Tailwind |
|----|----------|
| 0 | rounded-none |
| 2 | rounded-sm |
| 4 | rounded |
| 6 | rounded-md |
| 8 | rounded-lg |
| 12 | rounded-xl |
| 16 | rounded-2xl |
| 24 | rounded-3xl |
| 9999 | rounded-full |

### Per-corner Radius
```
rounded-t-lg    # top-left + top-right
rounded-r-lg    # top-right + bottom-right
rounded-b-lg    # bottom-left + bottom-right
rounded-l-lg    # top-left + bottom-left
rounded-tl-lg   # top-left only
rounded-tr-lg   # top-right only
rounded-br-lg   # bottom-right only
rounded-bl-lg   # bottom-left only
```

## Font Size

| px | Tailwind | Line Height |
|----|----------|-------------|
| 12 | text-xs | 1rem |
| 14 | text-sm | 1.25rem |
| 16 | text-base | 1.5rem |
| 18 | text-lg | 1.75rem |
| 20 | text-xl | 1.75rem |
| 24 | text-2xl | 2rem |
| 30 | text-3xl | 2.25rem |
| 36 | text-4xl | 2.5rem |
| 48 | text-5xl | 1 |
| 60 | text-6xl | 1 |
| 72 | text-7xl | 1 |
| 96 | text-8xl | 1 |
| 128 | text-9xl | 1 |

## Font Weight

| CSS Value | Tailwind |
|-----------|----------|
| 100 | font-thin |
| 200 | font-extralight |
| 300 | font-light |
| 400 | font-normal |
| 500 | font-medium |
| 600 | font-semibold |
| 700 | font-bold |
| 800 | font-extrabold |
| 900 | font-black |

## Box Shadow

| CSS | Tailwind |
|-----|----------|
| none | shadow-none |
| 0 1px 2px rgba(0,0,0,0.05) | shadow-sm |
| 0 1px 3px rgba(0,0,0,0.1) | shadow |
| 0 4px 6px rgba(0,0,0,0.1) | shadow-md |
| 0 10px 15px rgba(0,0,0,0.1) | shadow-lg |
| 0 20px 25px rgba(0,0,0,0.1) | shadow-xl |
| 0 25px 50px rgba(0,0,0,0.25) | shadow-2xl |
| inset 0 2px 4px rgba(0,0,0,0.05) | shadow-inner |

## Opacity

| CSS | Tailwind |
|-----|----------|
| 0 | opacity-0 |
| 0.05 | opacity-5 |
| 0.1 | opacity-10 |
| 0.2 | opacity-20 |
| 0.25 | opacity-25 |
| 0.3 | opacity-30 |
| 0.4 | opacity-40 |
| 0.5 | opacity-50 |
| 0.6 | opacity-60 |
| 0.7 | opacity-70 |
| 0.75 | opacity-75 |
| 0.8 | opacity-80 |
| 0.9 | opacity-90 |
| 0.95 | opacity-95 |
| 1 | opacity-100 |

## Flexbox

### Display
| CSS | Tailwind |
|-----|----------|
| display: flex | flex |
| display: inline-flex | inline-flex |

### Direction
| CSS | Tailwind |
|-----|----------|
| flex-direction: row | flex-row |
| flex-direction: row-reverse | flex-row-reverse |
| flex-direction: column | flex-col |
| flex-direction: column-reverse | flex-col-reverse |

### Justify Content
| CSS | Tailwind |
|-----|----------|
| justify-content: flex-start | justify-start |
| justify-content: center | justify-center |
| justify-content: flex-end | justify-end |
| justify-content: space-between | justify-between |
| justify-content: space-around | justify-around |
| justify-content: space-evenly | justify-evenly |

### Align Items
| CSS | Tailwind |
|-----|----------|
| align-items: flex-start | items-start |
| align-items: center | items-center |
| align-items: flex-end | items-end |
| align-items: baseline | items-baseline |
| align-items: stretch | items-stretch |

### Gap
| px | Tailwind |
|----|----------|
| 0 | gap-0 |
| 4 | gap-1 |
| 8 | gap-2 |
| 12 | gap-3 |
| 16 | gap-4 |
| 20 | gap-5 |
| 24 | gap-6 |
| 32 | gap-8 |

## Transitions

### Duration
| ms | Tailwind |
|----|----------|
| 75 | duration-75 |
| 100 | duration-100 |
| 150 | duration-150 |
| 200 | duration-200 |
| 300 | duration-300 |
| 500 | duration-500 |
| 700 | duration-700 |
| 1000 | duration-1000 |

### Timing Function
| CSS | Tailwind |
|-----|----------|
| linear | ease-linear |
| ease | ease-out |
| ease-in | ease-in |
| ease-out | ease-out |
| ease-in-out | ease-in-out |

### Transition Property
| CSS | Tailwind |
|-----|----------|
| none | transition-none |
| all | transition-all |
| colors | transition-colors |
| opacity | transition-opacity |
| transform | transition-transform |
