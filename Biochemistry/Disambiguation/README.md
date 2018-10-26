This is just a draft until I sort out my thoughts.

When correcting the biochemistry, either by merging compounds or disambiguating/splitting compounds that shouldn't have been merged, the first level at which the compounds need to be merged or split is at the level of aliases, hence the reason for these files. They contain the reaction-compound links from most of the files that were originally used to generate the original biochemistry. It then follows that, upon merging or splitting a compound, these files are used to identify the reactions that should be associated with the compounds. This is particularly pertinent as the disambiguation of a compound into two separate compounds means one must find the right reactions to which each of the two new compounds belong.

Merging and Disambiguation starts with Aliases, but after the aliases, the biochemistry, as in the compounds and then reactions, are handled seaparately from the chemical structures, for which the appropriate changes should also be made.

Finally, no commit will be merged until all affected compounds have had their formulas updated directly from the chemical structures, where possible, and all affected reactions have been re-balanced to check.