import logging
from typing import Optional, Dict, Any
from datetime import datetime

from google.cloud.firestore import Client
from django.conf import settings

from config.firebase_config import get_firestore_client

logger = logging.getLogger(__name__)

class FirestoreUserService:
    
  def __init__(self):
    self.db: Client = get_firestore_client()
    self.users_collection = settings.FIREBASE_COLLECTION_USERS
    self.avatars_collection = settings.FIREBASE_COLLECTION_AVATARS
    
  def create_user_avatar(self, user_id: int, avatar_base64: str) -> Optional[str]:
    try:
      avatar_data = {
        'user_id': str(user_id),
        'avatar_base64': avatar_base64,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow(),
        'version': 1,
        'is_active': True
      }

      doc_ref = self.db.collection(self.avatars_collection).document()
      doc_ref.set(avatar_data)

      user_data = {
        'current_avatar_id': doc_ref.id,
        'updated_at': datetime.utcnow()
      }
            
      user_doc_ref = self.db.collection(self.users_collection).document(str(user_id))
      user_doc_ref.set(user_data, merge=True)
      
      logger.info(f"Avatar stored in Firestore for user {user_id}, doc_id: {doc_ref.id}")
      return doc_ref.id
            
    except Exception as e:
      logger.error(f"Error storing avatar in Firestore for user {user_id}: {e}")
      return None
    
  def get_user_avatar(self, user_id: int) -> Optional[str]:
    try:
      user_doc = self.db.collection(self.users_collection).document(str(user_id)).get()
            
      if not user_doc.exists:
        logger.warning(f"User {user_id} not found in Firestore")
        return None
            
      user_data = user_doc.to_dict()
      avatar_id = user_data.get('current_avatar_id')
            
      if not avatar_id:
        return None
            
      avatar_doc = self.db.collection(self.avatars_collection).document(avatar_id).get()
            
      if not avatar_doc.exists:
        logger.warning(f"Avatar {avatar_id} not found for user {user_id}")
        return None
            
      avatar_data = avatar_doc.to_dict()
      return avatar_data.get('avatar_base64')
            
    except Exception as e:
      logger.error(f"Error getting avatar from Firestore for user {user_id}: {e}")
      return None
    
  def update_user_avatar(self, user_id: int, avatar_base64: str) -> bool:
    try:
      user_doc_ref = self.db.collection(self.users_collection).document(str(user_id))
      user_doc = user_doc_ref.get()
            
      user_data = user_doc.to_dict() if user_doc.exists else {}
      current_version = user_data.get('version', 0) if user_data else 0

      if user_data and user_data.get('current_avatar_id'):
        old_avatar_ref = self.db.collection(self.avatars_collection).document(
          user_data['current_avatar_id']
        )
        old_avatar_ref.update({
          'is_active': False,
          'updated_at': datetime.utcnow()
        })

      new_avatar_data = {
        'user_id': str(user_id),
        'avatar_base64': avatar_base64,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow(),
        'version': current_version + 1,
        'is_active': True
      }
      
      new_avatar_ref = self.db.collection(self.avatars_collection).document()
      new_avatar_ref.set(new_avatar_data)
            
      user_doc_ref.set({
        'current_avatar_id': new_avatar_ref.id,
        'updated_at': datetime.utcnow(),
        'version': current_version + 1
      }, merge=True)
            
      logger.info(f"Avatar updated for user {user_id}, new doc_id: {new_avatar_ref.id}")
      return True
            
    except Exception as e:
      logger.error(f"Error updating avatar in Firestore for user {user_id}: {e}")
      return False
    
  def delete_user_avatar(self, user_id: int) -> bool:
    try:
      user_doc_ref = self.db.collection(self.users_collection).document(str(user_id))
      user_doc = user_doc_ref.get()
            
      if not user_doc.exists:
        return True
            
      user_data = user_doc.to_dict()
      avatar_id = user_data.get('current_avatar_id')
            
      if avatar_id:
        avatar_ref = self.db.collection(self.avatars_collection).document(avatar_id)
        avatar_ref.update({
          'is_active': False,
          'updated_at': datetime.utcnow()
        })
            
      user_doc_ref.update({
        'current_avatar_id': None,
        'updated_at': datetime.utcnow()
      })
            
      logger.info(f"Avatar deleted for user {user_id}")
      return True
            
    except Exception as e:
      logger.error(f"Error deleting avatar from Firestore for user {user_id}: {e}")
      return False