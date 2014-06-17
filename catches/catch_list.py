from collections import OrderedDict
import copy
import itertools
from .handler import base_errors, ErrorsHandler


#Try/catch declarations
class CatchList(object):

    def __init__(self, catches=()):
        self._catches = []
        self._errors_catch = OrderedDict()
        self.add(*catches)

    def add(self, *catches):
        '''Move catch clauses with lower class hiearchy on top of their base classes.'''
        for catch in catches:
            existing_catches = _get_existing_catches(catch, self._get_errors_catches(catch.errors))
            if existing_catches:
                self._split_existing(_error_or_base_catches(catch, existing_catches))
            else:
                self._append(catch)

    def _append(self, catch):
        self._catches.append(catch)
        for error_class in catch.errors:
            if not error_class in self._errors_catch:
                self._errors_catch[error_class] = catch

    def top(self, *catches):
        '''Move catch clauses with higher class hiearchy on top of their sub classes.'''
        for catch in catches:
            existing_catches = _get_existing_catches(catch, self._get_subclasses_catches(catch.errors))
            if existing_catches:
                self._split_existing(_error_or_subclasses_catches(catch, existing_catches))
            else:
                self._append(catch)

    def _get_subclasses_catches(self, errors):
        base_handlers = OrderedDict()

        for error_class in self.classes:
            catch = self._errors_catch[error_class]
            base_handlers[error_class] = catch
            for base_error in base_errors(error_class):
                if base_error in errors and not base_error in base_handlers:
                    base_handlers[base_error] = catch

        return base_handlers

    def _split_existing(self, matching_catches):
        for existing, matching, remaining in matching_catches:
            position = self._catches.index(existing)

            if remaining.errors:
                self._catches[position] = remaining
                self._catches = self._catches[:position] + [matching] + self._catches[position:]
            else:
                self._catches[position] = matching

            for error_class in matching.errors:
                self._errors_catch[error_class] = matching

    def _get_errors_catches(self, errors):
        existing_handlers = OrderedDict()

        for error_class in errors:
            declaration = self._get_base_error_catch(error_class)

            if declaration:
                existing_handlers[error_class] = declaration

        return existing_handlers

    def _get_base_error_catch(self, error_class):
        error_definition = self._errors_catch.get(error_class)

        if not error_definition:
            for base_error in self._base_errors(error_class):
                error_definition = self._errors_catch.get(base_error)
                if error_definition:
                    return error_definition
        return error_definition

    def _base_errors(self, error):
        '''Resolve a mapping to an exception in the same order errors are listed'''
        error_mro = (error_class for error_class in base_errors(error) if error_class in self._errors_catch)
        return sorted(error_mro, key=lambda e: self._catches.index(self._errors_catch[e]))

    def get(self, error_class):
        return self._errors_catch.get(error_class)

    def remove_error(self, *error_classes):
        removed_catches = self._remove_errors_from_catches(error_classes)
        return removed_catches

    def remove_catch(self, *catches):
        removed = []
        for catch in catches:
            removed += self._remove_errors_from_catches(catch.errors, with_handler=catch.handler)
        return tuple(removed)

    def _remove_errors_from_catches(self, error_classes, with_handler=None):
        removed = []

        for position, catch in enumerate(self._catches):
            if not with_handler or with_handler == catch.handler:
                matching = [error for error in catch.errors if error in error_classes]

                if matching:
                    if len(matching) < len(catch.errors):
                        self._catches[position] = self._create_catch_for_remaining(catch, matching)
                    else:
                        del self._catches[position]

                    self._remove_errors_mapping(matching)
                    removed.append(ErrorsHandler(matching, catch.handler))

        return tuple(removed)

    def _create_catch_for_remaining(self, catch, error_classes):
        remaining = [error for error in catch.errors if not error in error_classes]
        catch = ErrorsHandler(remaining, catch.handler)
        for error_class in remaining:
            self._errors_catch[error_class] = catch
        return catch

    def _remove_errors_mapping(self, error_classes):
        for error_class in error_classes:
            if error_class in self._errors_catch:
                del self._errors_catch[error_class]

    @property
    def classes(self):
        return tuple(sorted(self._errors_catch.keys(), key=lambda e: self._catches.index(self._errors_catch[e])))

    @property
    def catches(self):
        return tuple(self._catches)

    def __iter__(self):
        return iter(self._catches)

    def __len__(self):
        return len(self._catches)

    def __contains__(self, catch):
        return catch in self._catches

    def __str__(self):
        return '\n'.join((str(declaration) for declaration in self._catches))

    def __copy__(self):
        catches_copy = self.__class__()
        catches_copy._catches = list(self._catches)
        catches_copy._errors_catch = OrderedDict(self._errors_catch)
        return catches_copy

    def copy(self):
        return copy.copy(self)

    def copy_with(self, *errors_handlers):
        catches_copy = self.copy()

        for catch in errors_handlers:
            catches_copy.add(catch)

        return catches_copy


def _get_existing_catches(catch, catches):
    existing_handlers = itertools.groupby(catch.errors, key=lambda x: catches.get(x))

    existing_catches = []
    for existing, group in existing_handlers:
        if existing:
            existing_catches.append((existing, list(group)))

    return existing_catches


def _error_or_base_catches(catch, existing_catches):
    return iter(_match_catches(catch, existing_catches, matcher=_base_classes_or_diff_handler))


def _match_catches(catch, existing_catches, matcher):
    for existing, group_errors in existing_catches:
        matching = matcher(catch, existing, group_errors)

        remaining = [error for error in existing.errors if not error in matching] if matching else []

        if matching:
            yield existing, ErrorsHandler(matching, catch.handler), ErrorsHandler(remaining, existing.handler)


def _error_or_subclasses_catches(catch, existing_catches):
    return iter(_match_catches(catch, existing_catches, matcher=_sub_classes_or_diff_handler))


def _base_classes_or_diff_handler(catch, existing, group_errors):
    matching = []
    for error in group_errors:
        catch_errors_matching = existing.matching(error)
        for catch_error in catch_errors_matching:
            if existing.handler != catch.handler or not catch_error == error:
                matching.append(error)
    return matching


def _sub_classes_or_diff_handler(catch, existing, group_errors):
    matching = []
    for error in group_errors:
        if not error in existing.errors or catch.handler != existing.handler:
            matching.append(error)
    return matching
