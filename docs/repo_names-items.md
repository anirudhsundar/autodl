# Untitled object in Simple to to download and manage latest releases from github Schema

```txt
undefined#/items
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                        |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :-------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [repo\_names.schema.json\*](../out/repo_names.schema.json "open original schema") |

## items Type

`object` ([Details](repo_names-items.md))

# items Properties

| Property                                | Type      | Required | Nullable       | Defined by                                                                                                                                                     |
| :-------------------------------------- | :-------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [name](#name)                           | `string`  | Required | cannot be null | [Simple to to download and manage latest releases from github](repo_names-items-properties-name.md "undefined#/items/properties/name")                         |
| [user](#user)                           | `string`  | Required | cannot be null | [Simple to to download and manage latest releases from github](repo_names-items-properties-user.md "undefined#/items/properties/user")                         |
| [repo](#repo)                           | `string`  | Required | cannot be null | [Simple to to download and manage latest releases from github](repo_names-items-properties-repo.md "undefined#/items/properties/repo")                         |
| [file\_pattern](#file_pattern)          | `string`  | Required | cannot be null | [Simple to to download and manage latest releases from github](repo_names-items-properties-file_pattern.md "undefined#/items/properties/file_pattern")         |
| [bin\_dir\_pattern](#bin_dir_pattern)   | `string`  | Required | cannot be null | [Simple to to download and manage latest releases from github](repo_names-items-properties-bin_dir_pattern.md "undefined#/items/properties/bin_dir_pattern")   |
| [uncompress\_cmd](#uncompress_cmd)      | `string`  | Optional | cannot be null | [Simple to to download and manage latest releases from github](repo_names-items-properties-uncompress_cmd.md "undefined#/items/properties/uncompress_cmd")     |
| [uncompress](#uncompress)               | `boolean` | Required | cannot be null | [Simple to to download and manage latest releases from github](repo_names-items-properties-uncompress.md "undefined#/items/properties/uncompress")             |
| [uncompress\_flags](#uncompress_flags)  | `string`  | Optional | cannot be null | [Simple to to download and manage latest releases from github](repo_names-items-properties-uncompress_flags.md "undefined#/items/properties/uncompress_flags") |
| [tag\_replace](#tag_replace)            | `array`   | Optional | cannot be null | [Simple to to download and manage latest releases from github](repo_names-items-properties-tag_replace.md "undefined#/items/properties/tag_replace")           |
| [copy\_to\_bin](#copy_to_bin)           | `boolean` | Optional | cannot be null | [Simple to to download and manage latest releases from github](repo_names-items-properties-copy_to_bin.md "undefined#/items/properties/copy_to_bin")           |
| [releases](#releases)                   | `string`  | Optional | cannot be null | [Simple to to download and manage latest releases from github](repo_names-items-properties-releases.md "undefined#/items/properties/releases")                 |
| [copy\_source\_name](#copy_source_name) | `string`  | Optional | cannot be null | [Simple to to download and manage latest releases from github](repo_names-items-properties-copy_source_name.md "undefined#/items/properties/copy_source_name") |
| [chmod](#chmod)                         | `string`  | Optional | cannot be null | [Simple to to download and manage latest releases from github](repo_names-items-properties-chmod.md "undefined#/items/properties/chmod")                       |

## name

Name of the final binary. Eg: `gh` for the github cli downloaded from the releases of <https://github.com/cli/cli>

`name`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [Simple to to download and manage latest releases from github](repo_names-items-properties-name.md "undefined#/items/properties/name")

### name Type

`string`

## user

The user/organization part of github url. Eg: `sharkdp` in the URL <https://github.com/sharkdp/bat>

`user`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [Simple to to download and manage latest releases from github](repo_names-items-properties-user.md "undefined#/items/properties/user")

### user Type

`string`

## repo

The repository part of github url. Eg: `bat` in the URL <https://github.com/sharkdp/bat>

`repo`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [Simple to to download and manage latest releases from github](repo_names-items-properties-repo.md "undefined#/items/properties/repo")

### repo Type

`string`

## file\_pattern

The filename to be downloaded with ### replacing the version. Eg: `gh_2.13.0_linux_amd64.tar.gz` becomes `gh_###_linux_amd64.tar.gz`

`file_pattern`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [Simple to to download and manage latest releases from github](repo_names-items-properties-file_pattern.md "undefined#/items/properties/file_pattern")

### file\_pattern Type

`string`

## bin\_dir\_pattern

The directory path to bin, created after uncompressing. Eg: `broot_all/build/x86_64-unknown-linux-musl` if path to bin directory from extracted root directory is `broot_all/build/x86_64-unknown-linux-musl/bin`

`bin_dir_pattern`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [Simple to to download and manage latest releases from github](repo_names-items-properties-bin_dir_pattern.md "undefined#/items/properties/bin_dir_pattern")

### bin\_dir\_pattern Type

`string`

## uncompress\_cmd

Command to use if the downloaded file has to be uncompressed automatically. Eg: `tar` or `unzip`

`uncompress_cmd`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [Simple to to download and manage latest releases from github](repo_names-items-properties-uncompress_cmd.md "undefined#/items/properties/uncompress_cmd")

### uncompress\_cmd Type

`string`

## uncompress

Whether to uncompress the downloaded file. The `uncompress_cmd` and `uncompress_flags` keys are not used if this is false

`uncompress`

*   is required

*   Type: `boolean`

*   cannot be null

*   defined in: [Simple to to download and manage latest releases from github](repo_names-items-properties-uncompress.md "undefined#/items/properties/uncompress")

### uncompress Type

`boolean`

## uncompress\_flags

Flags/options to pass to the uncompress\_cmd if it is used. Eg: `zxf` for tar command to extract a `.tar.gz` file

`uncompress_flags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [Simple to to download and manage latest releases from github](repo_names-items-properties-uncompress_flags.md "undefined#/items/properties/uncompress_flags")

### uncompress\_flags Type

`string`

## tag\_replace

Sometimes the tag part of the URL contains some extra characters added like v1.4.0 for version 1.4.0. Here the character 'v' would only be present in the tag and not in the filename, and hence has to be removed from the file name when generating the URL for download

`tag_replace`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [Simple to to download and manage latest releases from github](repo_names-items-properties-tag_replace.md "undefined#/items/properties/tag_replace")

### tag\_replace Type

`string[]`

### tag\_replace Constraints

**maximum number of items**: the maximum number of items for this array is: `2`

**minimum number of items**: the minimum number of items for this array is: `2`

## copy\_to\_bin

If there is just a single binary, it could be copied directly to \~/.bin which would already be in the PATH. This can be used for smaller tools that only contain a single binary and no dependencies

`copy_to_bin`

*   is optional

*   Type: `boolean`

*   cannot be null

*   defined in: [Simple to to download and manage latest releases from github](repo_names-items-properties-copy_to_bin.md "undefined#/items/properties/copy_to_bin")

### copy\_to\_bin Type

`boolean`

## releases

By default this is set to latest, and if we would like to use a different tag, that tag can be menstioned here

`releases`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [Simple to to download and manage latest releases from github](repo_names-items-properties-releases.md "undefined#/items/properties/releases")

### releases Type

`string`

### releases Default Value

The default value is:

```json
"latest"
```

## copy\_source\_name

If the original source filename is different from what we would like to use for the command, mention the source filename here

`copy_source_name`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [Simple to to download and manage latest releases from github](repo_names-items-properties-copy_source_name.md "undefined#/items/properties/copy_source_name")

### copy\_source\_name Type

`string`

## chmod

If you would like to update permissions for the copied binary, pass the chmod flags here

`chmod`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [Simple to to download and manage latest releases from github](repo_names-items-properties-chmod.md "undefined#/items/properties/chmod")

### chmod Type

`string`
