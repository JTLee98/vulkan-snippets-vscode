# generate the json for parameter-structs.code-snippets 
# from the vulkan API registry file vk.xml

import json
import xml.etree.ElementTree as ET
from pathlib import Path

# open output file
outf_path = Path(__file__).parent.parent / 'snippets' / 'parameter-structs.code-snippets'
outf = open(outf_path, "a")
outf.write("{")

# try to parse vk.xml
vk_xml_file = Path(__file__).parent / "vk.xml"
try:
  tree = ET.parse(vk_xml_file)
except Exception as e:
  print(f"vk.xml parse error : {e}")
  exit(1)

### --- VULKAN STRUCTS --- ###

# the vk.xml file specifies structs using the <type category="struct"> tag, 
# with struct members as their children with the <member> tag

# example for VkDeviceCreateInfo:
# <type category="struct" name="VkDeviceCreateInfo">
#     <member values="VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO"><type>VkStructureType</type> <name>sType</name></member>
#     <member optional="true">const <type>void</type>*     <name>pNext</name></member>
#     <member optional="true"><type>VkDeviceCreateFlags</type>    <name>flags</name></member>
#     <member><type>uint32_t</type>        <name>queueCreateInfoCount</name></member>
#     <member len="queueCreateInfoCount">const <type>VkDeviceQueueCreateInfo</type>* <name>pQueueCreateInfos</name></member>
#     <member optional="true" deprecated="ignored"><type>uint32_t</type>               <name>enabledLayerCount</name></member>
#     <member len="enabledLayerCount,null-terminated" deprecated="ignored">const <type>char</type>* const*      <name>ppEnabledLayerNames</name><comment>Ordered list of layer names to be enabled</comment></member>
#     <member optional="true"><type>uint32_t</type>               <name>enabledExtensionCount</name></member>
#     <member len="enabledExtensionCount,null-terminated">const <type>char</type>* const*      <name>ppEnabledExtensionNames</name></member>
#     <member optional="true">const <type>VkPhysicalDeviceFeatures</type>* <name>pEnabledFeatures</name></member>
# </type>

# the following attributes in the <type> tags are relevant here:
# - 'returnedonly'
# - 'structextends'
# - 'deprecated'
# the following attributes in the <member> tags are relevant here:
# - 'optional'
# - 'deprecated'

# get all structs
vkstructs = tree.getroot().find("types").findall("type[@category='struct']")
# generate struct snippets
for struct in vkstructs:
  # skip return only or deprecated structs
  if struct.get("returnedonly") or struct.get("deprecated"):
    continue

  # TODO: handle inherited structs ('structextends')

  # Create the VS Code snippet template
  # TODO: provide options for formatting brackets
  struct_name = struct.get("name") or struct.findtext("name")
  snippet_body = [f"{struct_name} ${{1:struct_name}} = {{"]
  # struct members
  idx = 1
  for member in struct.findall("member"):
    # skip deprecated members
    if member.get("deprecated", False):
      continue

    # get name
    m_name = member.find("name").text

    # create snippet
    # TODO: provide more options for indentation
    member_snippet = f"\t.{m_name} = "
    # sType: autocomplete value
    if (m_name == 'sType'):
      member_snippet += member.get("values", "") + ","
    # pNext: set to nullptr by default  
    elif (m_name == 'pNext'):
      member_snippet += "nullptr,"
    # other members
    else:
      # add type specifier
      # TODO: make this optional
      m_type = "".join(member.itertext())
      m_type = m_type[:m_type.find(m_name)]
      idx += 1
      member_snippet += f"${idx}, // {m_type.strip()}"

    # deal with optional members
    # TODO: provide more options for dealing with optional members in extension settings
    # TODO: provide option to switch this off
    if member.get("optional") == "true":
      member_snippet += " // [OPTIONAL]"
    
    # add comments
    # TODO: provide option to switch this off
    comment_tag = member.find("comment")
    if comment_tag != None: 
      if comment_tag.text != None: 
        member_snippet += " // " + comment_tag.text.strip()
    
    snippet_body.append(member_snippet)
  snippet_body.append("};")

  # write to snippets file
  vkstruct_snippet = {
    struct_name : {
      "prefix": struct_name,
      "body": snippet_body
    }  
  }
  outf.write(json.dumps(vkstruct_snippet)[1:-1] + ",\n")

# close json array
outf.write("}")

### --- VULKAN COMMANDS--- ###

# TODO: generate snippets with corresponding parameter structs from vulkan commands

# vk.xml specifies vulkan commands with a <command> tag, which contains 
# vulkan command format in vk.xml:
# <command successcodes="VK_SUCCESS" errorcodes="VK_ERROR_OUT_OF_HOST_MEMORY,VK_ERROR_OUT_OF_DEVICE_MEMORY,VK_ERROR_INITIALIZATION_FAILED,VK_ERROR_LAYER_NOT_PRESENT,VK_ERROR_EXTENSION_NOT_PRESENT,VK_ERROR_INCOMPATIBLE_DRIVER">
#     <proto><type>VkResult</type> <name>vkCreateInstance</name></proto>
#     <param>const <type>VkInstanceCreateInfo</type>* <name>pCreateInfo</name></param>
#     <param optional="true">const <type>VkAllocationCallbacks</type>* <name>pAllocator</name></param>
#     <param><type>VkInstance</type>* <name>pInstance</name></param>
# </command>

# get all commands
# vkcommands = tree.getroot().find("commands").findall("command")