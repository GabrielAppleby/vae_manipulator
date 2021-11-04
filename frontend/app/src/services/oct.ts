import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import {API_URL} from "../env";

export interface OCT {
    uid: number;
    label: string;
    url: string;
    x: number;
    y: number;
}

type OCTs = OCT[];

// Define a service using a base URL and expected endpoints
export const octAPI = createApi({
    baseQuery: fetchBaseQuery({ baseUrl: API_URL + 'api/duke' }),
    tagTypes: [],
    endpoints: (builder) => ({
        getOCTByID: builder.query<OCT, number>({
            query: (id: number) => `/${id}`,
        }),
        getOCTs: builder.query<OCTs, void>({
            query: () => '',
        }),
    }),
})

// Export hooks for usage in functional components
export const { useGetOCTByIDQuery,  useGetOCTsQuery} = octAPI
