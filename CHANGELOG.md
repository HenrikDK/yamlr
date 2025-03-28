# Changelog

## 2025-03-28:
- Changed: Made validators more flexible, no more classes & inheritance, just function pointers and native collection types.
- Changed: Removed use of eval and compile of ast trees to setup validator (improving security concerns greatly) 
- Added: debug trace for validation flow
- Added: support for keyed 'subset' and keyed 'any' validator types to avoid incorrect error messages.
