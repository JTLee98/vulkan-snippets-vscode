# Vulkan C++ Code Snippet Generator Extension for VS Code

work in progress

## Planned Features
### Struct Based Parameters Snippets:

vulkan has a ton of struct based parameter design, i.e. arguments are packed into dedicated structs for each function. 

For example, `vkCreateInstance()` takes a single dedicated `VkInstanceCreateInfo` struct type as a parameter and this struct contains the actual arguments for the function:
```cpp
// package the arguments into a VkInstanceCreateInfo struct
VkInstanceCreateInfo createInfo = {
    .sType = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO;
    .pApplicationInfo = &appInfo;
    .enabledExtensionCount = 3;
    .ppEnabledExtensionNames = extnames;
    .enabledLayerCount = 5;
    .ppEnabledLayerNames = layernames;
};
// pass the struct into the vkCreateInstance() api call
VkInstance instance;
vkCreateInstance(&createInfo, nullptr, &instance);
```

This extension will generate a code snippet of the necessary parameter struct (e.g. `VkInstanceCreateInfo`) when it detects the vulkan function that requires it (e.g. `vkCreateInstance()`).

### other useful features
TBA!

## Contributions

contributions are welcome!
