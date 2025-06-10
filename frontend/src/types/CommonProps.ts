import {
  Infer,
  any,
  array,
  boolean,
  nullable,
  object,
  optional,
} from 'superstruct';
import { User } from './User';
import { FlashMessage } from './FlashMessage';

export type CommonProps = Infer<typeof CommonProps>;

export const CommonProps = object({
  is_authenticated: boolean(),
  user: optional(nullable(User)),
  has_add_permission: optional(boolean()),
  has_change_permission: optional(boolean()),
  flash_messages: optional(array(FlashMessage)),
  errors: optional(nullable(any())),
});
