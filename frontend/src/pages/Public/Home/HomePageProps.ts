import { CommonProps } from '@/types/CommonProps';
import {
  Infer,
  assign,
  number,
  object,
} from 'superstruct';


export const HomePageProps = assign(
  object({
    stats: object({
      test: number(),
    }),
  }),
  CommonProps,
);

export type HomePageProps = Infer<typeof HomePageProps>;
