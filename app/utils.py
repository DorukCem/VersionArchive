import hashlib
from typing import List
from . import models
import difflib

def create_object_oid(blob):
   return hashlib.sha1(blob).hexdigest()

def create_commit_oid(objects):
   return hashlib.sha1( "".join(sorted([obj.oid for obj in objects])).encode() ).hexdigest()

def merge_old_and_new_objects(old_objects : List[models.Object], new_objects : List[models.Object]):
   """
      Merge old objects and new objects by object.name
      if a file with the same name is in both lists, take the newer one
   """
   name_to_object = {obj.name : obj for obj in old_objects}
   for obj in new_objects:
      name_to_object[obj.name] = obj

   return list(name_to_object.values())


def diff_blobs(content_from, content_to, skip_headers= True):
   
   lines_from = content_from.decode("utf-8").splitlines()
   lines_to = content_to.decode("utf-8").splitlines()

   diff = difflib.unified_diff(lines_from, lines_to)

   if not skip_headers:
      for i,_ in enumerate(diff):
         if i == 2:
            break

   return '\n'.join(diff).encode("utf-8")